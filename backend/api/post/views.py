from datetime import datetime
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from api.user.models import User
from api.post.models import Post, Like, Comment, Save
from api.post.schemas import (
    PostResponse,
    PostUpdate,
    FeedResponse,
    LikeResponse,
    SaveResponse,
    CommentCreate,
    CommentResponse,
    CommentsResponse,
)
from api.user.auth import get_current_user
from api.cloudflare.r2_service import upload_media_file, delete_media_file, get_presigned_url

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse)
async def create_post(
    content: Optional[str] = Form(None),
    recipe_title: Optional[str] = Form(None),
    ingredients: Optional[str] = Form(None),
    instructions: Optional[str] = Form(None),
    cooking_time: Optional[int] = Form(None),
    servings: Optional[int] = Form(None),
    difficulty: Optional[str] = Form(None),
    cuisine_type: Optional[str] = Form(None),
    is_public: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new post with optional media upload"""
    if not any([content, recipe_title, image, video]):
        raise HTTPException(status_code=400, detail="Post must have at least content, recipe title, or media")

    if difficulty and difficulty.lower() not in ["easy", "medium", "hard"]:
        raise HTTPException(status_code=400, detail="Difficulty must be easy, medium, or hard")

    if image and video:
        raise HTTPException(status_code=400, detail="Please upload either an image or video, not both")

    image_key: Optional[str] = None
    video_key: Optional[str] = None

    # 1) Upload first
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

    # 2) Save DB, cleanup on failure
    try:
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
            image_url=image_key,   # storing object keys, not public URLs
            video_url=video_key,
            author_id=current_user.id,
        )

        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post

    except Exception as e:
        await db.rollback()
        # Best-effort cleanup of uploaded media
        try:
            if image_key:
                await delete_media_file(image_key)
            if video_key:
                await delete_media_file(video_key)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Post creation failed: {str(e)}")


@router.put("/{post_id}/media")
async def update_post_media(
    post_id: UUID,
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update media for an existing post"""

    # Load post
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.author_id == current_user.id)
    )
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")

    if not image and not video:
        raise HTTPException(status_code=400, detail="No media file provided")

    if image and video:
        raise HTTPException(status_code=400, detail="Please upload either an image or video, not both")

    try:
        # Delete old media if replacing
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
            post.image_url = file_key
            post.video_url = None

        if video:
            file_key, media_type = await upload_media_file(video, current_user.id)
            post.video_url = file_key
            post.image_url = None

        await db.commit()
        return {
            "message": "Media updated successfully",
            "image_url": post.image_url,
            "video_url": post.video_url,
            "old_media_deleted": old_media_deleted,
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Media update failed: {str(e)}")


@router.delete("/{post_id}")
async def delete_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete a post and async-delete its media"""

    try:
        result = await db.execute(
            select(Post).where(Post.id == post_id, Post.author_id == current_user.id)
        )
        post = result.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found or unauthorized")

        media_deletion_tasks = []
        if post.image_url:
            media_deletion_tasks.append(delete_media_file(post.image_url))
        if post.video_url:
            media_deletion_tasks.append(delete_media_file(post.video_url))

        post.is_active = False
        await db.commit()

        # fire-and-forget
        if media_deletion_tasks:
            import asyncio

            asyncio.create_task(asyncio.gather(*media_deletion_tasks, return_exceptions=True))

        return {"message": "Post deleted successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Post deletion failed: {str(e)}")


async def get_user_interactions(db: AsyncSession, user_id: UUID, post_ids: List[UUID]):
    """Get user's likes and saves for given posts"""
    try:
        likes_result = await db.execute(
            select(Like.post_id).where(Like.user_id == user_id, Like.post_id.in_(post_ids))
        )
        saves_result = await db.execute(
            select(Save.post_id).where(Save.user_id == user_id, Save.post_id.in_(post_ids))
        )

        liked_posts = {row[0] for row in likes_result.all()}
        saved_posts = {row[0] for row in saves_result.all()}
        return liked_posts, saved_posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User interaction retrieval failed: {str(e)}")


@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    cursor: Optional[UUID] = Query(None, description="Last post ID for pagination"),
    limit: int = Query(10, ge=1, le=50, description="Number of posts to fetch"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get paginated feed posts"""
    try:
        base_stmt = (
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.is_active == True, Post.is_public == True)
            .order_by(desc(Post.created_at))
        )

        if cursor:
            cursor_res = await db.execute(select(Post).where(Post.id == cursor))
            cursor_post = cursor_res.scalars().first()
            if cursor_post:
                base_stmt = base_stmt.where(Post.created_at < cursor_post.created_at)

        stmt = base_stmt.limit(limit + 1)
        res = await db.execute(stmt)
        posts = res.scalars().all()

        has_more = len(posts) > limit
        if has_more:
            posts = posts[:limit]

        post_ids = [p.id for p in posts]
        liked_posts, saved_posts = await get_user_interactions(db, current_user.id, post_ids)

        # decorate + presign
        for p in posts:
            p.is_liked = p.id in liked_posts
            p.is_saved = p.id in saved_posts
            if p.image_url:
                p.image_url = get_presigned_url(p.image_url)
            if p.video_url:
                p.video_url = get_presigned_url(p.video_url)

        next_cursor = posts[-1].id if posts else None

        return FeedResponse(posts=posts, has_more=has_more, next_cursor=next_cursor)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feed retrieval failed: {str(e)}")


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific post"""
    try:
        res = await db.execute(
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.id == post_id, Post.is_active == True)
        )
        post = res.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if not post.is_public and post.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        liked_posts, saved_posts = await get_user_interactions(db, current_user.id, [post_id])
        post.is_liked = post_id in liked_posts
        post.is_saved = post_id in saved_posts

        if post.image_url:
            post.image_url = get_presigned_url(post.image_url)
        if post.video_url:
            post.video_url = get_presigned_url(post.video_url)

        return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Post retrieval failed: {str(e)}")


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a post"""
    try:
        res = await db.execute(
            select(Post).where(Post.id == post_id, Post.author_id == current_user.id)
        )
        post = res.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found or unauthorized")

        update_data = post_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post, field, value)

        post.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(post)
        return post

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Post update failed: {str(e)}")


@router.post("/{post_id}/like", response_model=LikeResponse)
async def toggle_like(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle like on a post"""
    try:
        # post exists?
        res = await db.execute(select(Post).where(Post.id == post_id, Post.is_active == True))
        post = res.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        like_res = await db.execute(
            select(Like).where(Like.post_id == post_id, Like.user_id == current_user.id)
        )
        existing_like = like_res.scalars().first()

        if existing_like:
            await db.delete(existing_like)
            post.likes_count = max(0, post.likes_count - 1)
            liked = False
        else:
            new_like = Like(post_id=post_id, user_id=current_user.id)
            db.add(new_like)
            post.likes_count += 1
            liked = True

        await db.commit()
        return LikeResponse(liked=liked, likes_count=post.likes_count)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Post liking failed: {str(e)}")


@router.post("/{post_id}/save", response_model=SaveResponse)
async def toggle_save(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle save on a post"""
    try:
        res = await db.execute(select(Post).where(Post.id == post_id, Post.is_active == True))
        post = res.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        save_res = await db.execute(
            select(Save).where(Save.post_id == post_id, Save.user_id == current_user.id)
        )
        existing_save = save_res.scalars().first()

        if existing_save:
            await db.delete(existing_save)
            post.saves_count = max(0, post.saves_count - 1)
            saved = False
        else:
            new_save = Save(post_id=post_id, user_id=current_user.id)
            db.add(new_save)
            post.saves_count += 1
            saved = True

        await db.commit()
        return SaveResponse(saved=saved, saves_count=post.saves_count)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Post saving failed: {str(e)}")


@router.post("/{post_id}/comments", response_model=CommentResponse)
async def add_comment(
    post_id: UUID,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a comment to a post"""
    try:
        res = await db.execute(select(Post).where(Post.id == post_id, Post.is_active == True))
        post = res.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        db_comment = Comment(
            **comment_data.model_dump(),
            post_id=post_id,
            user_id=current_user.id,
        )
        db.add(db_comment)
        post.comments_count += 1
        await db.commit()
        await db.refresh(db_comment)

        # load with user relationship
        c_res = await db.execute(
            select(Comment)
            .options(selectinload(Comment.user))
            .where(Comment.id == db_comment.id)
        )
        comment_with_user = c_res.scalars().first()
        return comment_with_user

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Comment addition failed: {str(e)}")


@router.get("/{post_id}/comments", response_model=CommentsResponse)
async def get_comments(
    post_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get comments for a post (top-level only)"""
    try:
        # ensure post exists (optional)
        res = await db.execute(select(Post.id).where(Post.id == post_id, Post.is_active == True))
        if not res.scalar():
            raise HTTPException(status_code=404, detail="Post not found")

        comments_res = await db.execute(
            select(Comment)
            .options(selectinload(Comment.user), selectinload(Comment.replies))
            .where(
                Comment.post_id == post_id,
                Comment.is_active == True,
                Comment.parent_comment_id.is_(None),
            )
            .order_by(desc(Comment.created_at))
            .offset(offset)
            .limit(limit)
        )
        comments = comments_res.scalars().all()

        count_res = await db.execute(
            select(func.count())
            .select_from(Comment)
            .where(
                Comment.post_id == post_id,
                Comment.is_active == True,
                Comment.parent_comment_id.is_(None),
            )
        )
        total_count = count_res.scalar() or 0

        return CommentsResponse(comments=comments, total_count=total_count)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comment retrieval failed: {str(e)}")


@router.get("/users/{user_id}/posts", response_model=FeedResponse)
async def get_user_posts(
    user_id: UUID,
    cursor: Optional[UUID] = Query(None),
    limit: int = Query(12, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get posts by a specific user (public if not owner)"""
    try:
        stmt = (
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.author_id == user_id, Post.is_active == True)
        )

        if user_id != current_user.id:
            stmt = stmt.where(Post.is_public == True)

        stmt = stmt.order_by(desc(Post.created_at))

        if cursor:
            cursor_res = await db.execute(select(Post).where(Post.id == cursor))
            cursor_post = cursor_res.scalars().first()
            if cursor_post:
                stmt = stmt.where(Post.created_at < cursor_post.created_at)

        stmt = stmt.limit(limit + 1)
        res = await db.execute(stmt)
        posts = res.scalars().all()

        has_more = len(posts) > limit
        if has_more:
            posts = posts[:limit]

        post_ids = [p.id for p in posts]
        liked_posts, saved_posts = await get_user_interactions(db, current_user.id, post_ids)

        for p in posts:
            p.is_liked = p.id in liked_posts
            p.is_saved = p.id in saved_posts

        next_cursor = posts[-1].id if posts else None

        return FeedResponse(posts=posts, has_more=has_more, next_cursor=next_cursor)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Post retrieval failed: {str(e)}")
