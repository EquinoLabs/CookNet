from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import Optional, List
import asyncio
import traceback
from database.database import get_db
from api.user.models import User
from api.post.models import Post, Like, Comment, Save
from api.post.schemas import *
from api.user.auth import get_current_user
from api.cloudflare.r2_service import upload_media_file, delete_media_file, get_presigned_url

router = APIRouter(prefix="/api", tags=["posts"])

@router.post("/posts", response_model=PostResponse)
async def create_post(
    # Text data as form fields
    content: Optional[str] = Form(None),
    recipe_title: Optional[str] = Form(None),
    ingredients: Optional[str] = Form(None),
    instructions: Optional[str] = Form(None),
    cooking_time: Optional[int] = Form(None),
    servings: Optional[int] = Form(None),
    difficulty: Optional[str] = Form(None),
    cuisine_type: Optional[str] = Form(None),
    is_public: bool = Form(True),
    
    # Media files (optional)
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    
    # Dependencies
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new post with optional media upload"""

    # Validate that at least some content is provided
    if not any([content, recipe_title, image, video]):
        raise HTTPException(
            status_code=400, 
            detail="Post must have at least content, recipe title, or media"
        )
        
    # Validate difficulty if provided
    if difficulty and difficulty.lower() not in ['easy', 'medium', 'hard']:
        raise HTTPException(status_code=400, detail="Difficulty must be easy, medium, or hard")
    
    # Validate that only one media type is provided
    if image and video:
        raise HTTPException(status_code=400, detail="Please upload either an image or video, not both")
    
    # Upload media to Cloudflare if provided
    image_key = None
    video_key = None
    
    try:
        if image:
            object_key, media_type = await upload_media_file(image, current_user.id)
            if media_type == "image":
                image_key = object_key
        
        if video:
            object_key, media_type = await upload_media_file(video, current_user.id)
            if media_type == "video":
                video_key = object_key
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Media upload failed: {str(e)}")
    
    try:
        # Create post with all data
        db_post = Post(
            content=content,
            recipe_title=recipe_title,
            ingredients=ingredients,
            instructions=instructions,
            cooking_time=cooking_time,
            servings=servings,
            difficulty=difficulty.lower() if difficulty else None,
            cuisine_type=cuisine_type,
            is_public=is_public,
            image_url=image_key,
            video_url=video_key,
            author_id=current_user.id
        )
        
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)

        return db_post
    except Exception as e:
        # Delete uploaded files if DB operation failed
        if image_key:
            await delete_media_file(image_key)
        if video_key:
            await delete_media_file(video_key)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Post creation failed: {str(e)}")



@router.put("/posts/{post_id}/media")
async def update_post_media(
    post_id: int,
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update media for an existing post"""
    
    # Check if post exists and user owns it
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.author_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    
    if not image and not video:
        raise HTTPException(status_code=400, detail="No media file provided")
    
    if image and video:
        raise HTTPException(status_code=400, detail="Please upload either an image or video, not both")
    
    try:
        # Delete old media if exists
        old_media_deleted = []
        if post.image_url and image:
            if await delete_media_file(post.image_url):
                old_media_deleted.append("image")
        
        if post.video_url and video:
            if await delete_media_file(post.video_url):
                old_media_deleted.append("video")
        
        # Upload new media
        if image:
            file_key, media_type = await upload_media_file(image, current_user.id)
            post.image_url = file_key       # store only object key
            post.video_url = None

        if video:
            file_key, media_type = await upload_media_file(video, current_user.id)
            post.video_url = file_key       # store only object key
            post.image_url = None
        
        db.commit()
        
        return {
            "message": "Media updated successfully",
            "image_url": post.image_url,
            "video_url": post.video_url,
            "old_media_deleted": old_media_deleted
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Media update failed: {str(e)}")


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a post and its associated media"""
    
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.author_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    
    # Delete media from Cloudflare in background
    media_deletion_tasks = []
    if post.image_url:
        media_deletion_tasks.append(delete_media_file(post.image_url))
    if post.video_url:
        media_deletion_tasks.append(delete_media_file(post.video_url))
    
    # Soft delete post first
    post.is_active = False
    db.commit()
    
    # Delete media files asynchronously (don't wait for completion)
    if media_deletion_tasks:
        asyncio.create_task(asyncio.gather(*media_deletion_tasks, return_exceptions=True))
    
    return {"message": "Post deleted successfully"}


# Utility function to check user interactions
def get_user_interactions(db: Session, user_id: int, post_ids: List[int]):
    """Get user's likes and saves for given posts"""
    likes = db.query(Like.post_id).filter(
        Like.user_id == user_id,
        Like.post_id.in_(post_ids)
    ).all()
    
    saves = db.query(Save.post_id).filter(
        Save.user_id == user_id,
        Save.post_id.in_(post_ids)
    ).all()
    
    liked_posts = {like.post_id for like in likes}
    saved_posts = {save.post_id for save in saves}
    
    return liked_posts, saved_posts


@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    cursor: Optional[UUID] = Query(None, description="Last post ID for pagination"),
    limit: int = Query(10, ge=1, le=50, description="Number of posts to fetch"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get paginated feed posts"""
    
    query = db.query(Post).options(
        selectinload(Post.author)
    ).filter(
        Post.is_active == True,
        Post.is_public == True
    ).order_by(desc(Post.created_at))
    
    if cursor:
        cursor_post = db.query(Post).filter(Post.id == cursor).first()
        if cursor_post:
            query = query.filter(Post.created_at < cursor_post.created_at)
    
    posts = query.limit(limit + 1).all()
    
    has_more = len(posts) > limit
    if has_more:
        posts = posts[:limit]
    
    post_ids = [post.id for post in posts]
    liked_posts, saved_posts = get_user_interactions(db, current_user.id, post_ids)
    
    for post in posts:
        post.is_liked = post.id in liked_posts
        post.is_saved = post.id in saved_posts

        # Generate presigned URLs for private content
        if post.image_url:
            post.image_url = get_presigned_url(post.image_url)
        if post.video_url:
            post.video_url = get_presigned_url(post.video_url)
    
    next_cursor = posts[-1].id if posts else None
    
    return FeedResponse(
        posts=posts,
        has_more=has_more,
        next_cursor=next_cursor
    )


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific post"""
    
    post = db.query(Post).options(
        selectinload(Post.author)
    ).filter(
        Post.id == post_id,
        Post.is_active == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user can view this post
    if not post.is_public and post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get user interactions
    liked_posts, saved_posts = get_user_interactions(db, current_user.id, [post_id])
    post.is_liked = post_id in liked_posts
    post.is_saved = post_id in saved_posts
    
    return post


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a post"""
    
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.author_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    
    # Update post fields
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    
    return post


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a post"""
    
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.author_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    
    # Soft delete
    post.is_active = False
    db.commit()
    
    return {"message": "Post deleted successfully"}


@router.post("/posts/{post_id}/like", response_model=LikeResponse)
async def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle like on a post"""
    
    # Check if post exists
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.is_active == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user already liked this post
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()
    
    if existing_like:
        # Unlike
        db.delete(existing_like)
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        # Like
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        post.likes_count += 1
        liked = True
    
    db.commit()
    
    return LikeResponse(liked=liked, likes_count=post.likes_count)


@router.post("/posts/{post_id}/save", response_model=SaveResponse)
async def toggle_save(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle save on a post"""
    
    # Check if post exists
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.is_active == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user already saved this post
    existing_save = db.query(Save).filter(
        Save.post_id == post_id,
        Save.user_id == current_user.id
    ).first()
    
    if existing_save:
        # Unsave
        db.delete(existing_save)
        post.saves_count = max(0, post.saves_count - 1)
        saved = False
    else:
        # Save
        new_save = Save(post_id=post_id, user_id=current_user.id)
        db.add(new_save)
        post.saves_count += 1
        saved = True
    
    db.commit()
    
    return SaveResponse(saved=saved, saves_count=post.saves_count)


@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def add_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a comment to a post"""
    
    # Check if post exists
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.is_active == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create comment
    db_comment = Comment(
        **comment_data.model_dump(),
        post_id=post_id,
        user_id=current_user.id
    )
    
    db.add(db_comment)
    post.comments_count += 1
    db.commit()
    db.refresh(db_comment)
    
    # Load with user relationship
    comment_with_user = db.query(Comment).options(
        selectinload(Comment.user)
    ).filter(Comment.id == db_comment.id).first()
    
    return comment_with_user


@router.get("/posts/{post_id}/comments", response_model=CommentsResponse)
async def get_comments(
    post_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comments for a post"""
    
    # Check if post exists
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.is_active == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Get comments (only top-level comments, replies loaded separately)
    comments = db.query(Comment).options(
        selectinload(Comment.user),
        selectinload(Comment.replies)
    ).filter(
        Comment.post_id == post_id,
        Comment.is_active == True,
        Comment.parent_comment_id.is_(None)  # Top-level comments only
    ).order_by(desc(Comment.created_at)).offset(offset).limit(limit).all()
    
    # Get total count
    total_count = db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.is_active == True,
        Comment.parent_comment_id.is_(None)
    ).count()
    
    return CommentsResponse(comments=comments, total_count=total_count)


@router.get("/users/{user_id}/posts", response_model=FeedResponse)
async def get_user_posts(
    user_id: int,
    cursor: Optional[UUID] = Query(None),
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get posts by a specific user"""
    
    # Base query
    query = db.query(Post).options(
        selectinload(Post.author)
    ).filter(
        Post.author_id == user_id,
        Post.is_active == True
    )
    
    # If requesting other user's posts, only show public ones
    if user_id != current_user.id:
        query = query.filter(Post.is_public == True)
    
    query = query.order_by(desc(Post.created_at))
    
    # Cursor pagination
    if cursor:
        cursor_post = db.query(Post).filter(Post.id == cursor).first()
        if cursor_post:
            query = query.filter(Post.created_at < cursor_post.created_at)
    
    posts = query.limit(limit + 1).all()
    
    has_more = len(posts) > limit
    if has_more:
        posts = posts[:limit]
    
    # Get user interactions
    post_ids = [post.id for post in posts]
    liked_posts, saved_posts = get_user_interactions(db, current_user.id, post_ids)
    
    for post in posts:
        post.is_liked = post.id in liked_posts
        post.is_saved = post.id in saved_posts
    
    next_cursor = posts[-1].id if posts else None
    
    return FeedResponse(
        posts=posts,
        has_more=has_more,
        next_cursor=next_cursor
    )
