from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy import desc, func, and_, or_, select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List
from uuid import UUID
import re
from datetime import datetime

from database.database import get_db
from api.user.models import User
from api.community.models import Community, CommunityInvite, community_members
from api.community.schemas import *
from api.user.auth import get_current_user
from api.cloudflare.r2_service import upload_media_file

router = APIRouter(prefix="/communities", tags=["communities"])


def create_slug(name: str) -> str:
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug


async def get_community_or_404(db: AsyncSession, community_id: UUID, current_user: User = None):
    try:
        result = await db.execute(select(Community).where(Community.id == community_id))
        community = result.scalars().first()
        if not community:
            raise HTTPException(status_code=404, detail="Community not found")

        if community.is_private and current_user:
            result = await db.execute(
                select(community_members).where(
                    and_(
                        community_members.c.community_id == community_id,
                        community_members.c.user_id == current_user.id
                    )
                )
            )
            is_member = result.first()
            if not is_member and community.created_by_id != current_user.id:
                raise HTTPException(status_code=403, detail="Access denied to private community")

        return community
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Community lookup failed: {str(e)}")


@router.post("/", response_model=CommunityResponse, status_code=status.HTTP_201_CREATED)
async def create_community(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    rules: Optional[str] = Form(None),
    is_private: bool = Form(False),
    display_photo: Optional[UploadFile] = File(None),
    banner_photo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        community_data = CommunityCreate(
            name=name,
            description=description,
            category=category,
            rules=rules,
            is_private=is_private
        )

        base_slug = create_slug(community_data.name)
        slug, counter = base_slug, 1
        while (await db.execute(select(Community).where(Community.slug == slug))).scalars().first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        display_photo_url, banner_photo_url = None, None
        if display_photo:
            if not display_photo.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Display photo must be an image")
            url, _ = await upload_media_file(display_photo, current_user.id)
            display_photo_url = url
        if banner_photo:
            if not banner_photo.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Banner photo must be an image")
            url, _ = await upload_media_file(banner_photo, current_user.id)
            banner_photo_url = url

        db_community = Community(
            name=community_data.name,
            slug=slug,
            description=community_data.description,
            category=community_data.category,
            rules=community_data.rules,
            is_private=community_data.is_private,
            display_photo_url=display_photo_url,
            banner_photo_url=banner_photo_url,
            created_by_id=current_user.id,
            member_count=1
        )

        db.add(db_community)
        await db.commit()
        await db.refresh(db_community)

        await db.execute(
            insert(community_members).values(
                user_id=current_user.id,
                community_id=db_community.id,
                role="admin"
            )
        )
        await db.commit()

        result = await db.execute(
            select(Community).options(selectinload(Community.created_by)).where(Community.id == db_community.id)
        )
        return result.scalars().first()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Community creation failed: {str(e)}")


@router.get("/", response_model=CommunityListResponse)
async def get_communities(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    is_private: Optional[bool] = Query(None),
    sort_by: str = Query("created_at", regex="^(created_at|member_count|post_count|name)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    try:
        stmt = select(Community).options(selectinload(Community.created_by))
        if category:
            stmt = stmt.where(Community.category == category.lower())
        if search:
            stmt = stmt.where(or_(Community.name.ilike(f"%{search}%"), Community.description.ilike(f"%{search}%")))
        if is_private is not None:
            stmt = stmt.where(Community.is_private == is_private)

        sort_column = getattr(Community, sort_by)
        stmt = stmt.order_by(desc(sort_column) if sort_order == "desc" else sort_column)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await db.execute(count_stmt)).scalar()

        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)
        communities = (await db.execute(stmt)).scalars().all()

        return CommunityListResponse(
            communities=communities,
            total=total,
            page=page,
            size=size,
            total_pages=(total + size - 1) // size
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Community retrieval failed: {str(e)}")


@router.get("/{community_id}", response_model=CommunityDetailResponse)
async def get_community(
    community_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    try:
        community = await get_community_or_404(db, community_id, current_user)

        result = await db.execute(
            select(Community).options(
                selectinload(Community.created_by),
                selectinload(Community.members)
            ).where(Community.id == community_id)
        )
        community = result.scalars().first()

        is_member, user_role = False, None
        if current_user:
            result = await db.execute(
                select(community_members).where(
                    and_(
                        community_members.c.community_id == community_id,
                        community_members.c.user_id == current_user.id
                    )
                )
            )
            membership = result.first()
            if membership:
                is_member, user_role = True, membership.role

        response_data = community.__dict__
        response_data['is_member'] = is_member
        response_data['user_role'] = user_role
        return CommunityDetailResponse(**response_data)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Community detail retrieval failed: {str(e)}")


@router.post("/{community_id}/join", response_model=MembershipResponse)
async def join_community(
    community_id: UUID,
    request: JoinCommunityRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        community = await get_community_or_404(db, community_id)

        result = await db.execute(
            select(community_members).where(
                and_(
                    community_members.c.community_id == community_id,
                    community_members.c.user_id == current_user.id
                )
            )
        )
        if result.first():
            raise HTTPException(status_code=400, detail="Already a member of this community")

        if community.is_private:
            if not request.invite_code:
                raise HTTPException(status_code=403, detail="Invite code required for private community")

            result = await db.execute(
                select(CommunityInvite).where(
                    and_(
                        CommunityInvite.community_id == community_id,
                        CommunityInvite.invite_code == request.invite_code,
                        CommunityInvite.is_active == True,
                        or_(
                            CommunityInvite.expires_at.is_(None),
                            CommunityInvite.expires_at > datetime.utcnow()
                        ),
                        CommunityInvite.current_uses < CommunityInvite.max_uses
                    )
                )
            )
            invite = result.scalars().first()
            if not invite:
                raise HTTPException(status_code=403, detail="Invalid or expired invite code")

            invite.current_uses += 1
            if invite.current_uses >= invite.max_uses:
                invite.is_active = False

        await db.execute(
            insert(community_members).values(
                user_id=current_user.id,
                community_id=community_id,
                role="member"
            )
        )

        community.member_count += 1
        await db.commit()

        return MembershipResponse(
            community_id=community_id,
            user_id=current_user.id,
            role="member",
            joined_at=datetime.utcnow()
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Join community failed: {str(e)}")


@router.delete("/{community_id}/leave")
async def leave_community(
    community_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        community = await get_community_or_404(db, community_id)

        result = await db.execute(
            select(community_members).where(
                and_(
                    community_members.c.community_id == community_id,
                    community_members.c.user_id == current_user.id
                )
            )
        )
        membership = result.first()
        if not membership:
            raise HTTPException(status_code=400, detail="Not a member of this community")

        if community.created_by_id == current_user.id:
            raise HTTPException(status_code=400, detail="Community creator cannot leave. Transfer ownership or delete community.")

        await db.execute(
            delete(community_members).where(
                and_(
                    community_members.c.community_id == community_id,
                    community_members.c.user_id == current_user.id
                )
            )
        )

        community.member_count -= 1
        await db.commit()

        return {"message": "Successfully left community"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Leave community failed: {str(e)}")


@router.delete("/{community_id}")
async def delete_community(
    community_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        community = await get_community_or_404(db, community_id)

        if community.created_by_id != current_user.id:
            raise HTTPException(status_code=403, detail="Only community creator can delete community")

        await db.delete(community)
        await db.commit()

        return {"message": "Community deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete community failed: {str(e)}")


@router.get("/{community_id}/members", response_model=List[CommunityMember])
async def get_community_members(
    community_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    try:
        await get_community_or_404(db, community_id, current_user)

        offset = (page - 1) * size
        stmt = (
            select(User, community_members.c.joined_at, community_members.c.role)
            .join(community_members, User.id == community_members.c.user_id)
            .where(community_members.c.community_id == community_id)
            .order_by(community_members.c.joined_at.desc())
            .offset(offset)
            .limit(size)
        )

        result = await db.execute(stmt)
        members = []
        for user, joined_at, role in result.all():
            members.append(
                CommunityMember(
                    id=user.id,
                    username=user.username,
                    display_name=getattr(user, 'display_name', None),
                    profile_picture_url=getattr(user, 'profile_picture_url', None),
                    joined_at=joined_at,
                    role=role
                )
            )
        return members
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Community members retrieval failed: {str(e)}")
