from datetime import datetime
from sqlalchemy.orm import selectinload
from routes.v1.post.dto.post_request import PostRequest
from schemas.post import Post
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select
from typing import List
from routes.v1.post.dto.post_update import PostUpdate 
from utils.errors.index import NotFound
import base64

class PostRepository : 

    def __init__(self) : 
        pass

    async def find_all(self, limit : int, cursor : str | None, db : AsyncSession) -> List[Post] : 

        statement = select(Post).options(selectinload(Post.user)).order_by(desc(Post.created_at)).limit(limit=limit+1)

        if cursor : 
            last_date_str : str = base64.urlsafe_b64decode(cursor.encode()).decode()
            last_date : datetime = datetime.fromisoformat(last_date_str)
            statement = statement.where(Post.created_at < last_date)

        result = await db.execute(statement=statement)
        posts = result.scalars().all()

        if not posts : 
            raise NotFound("Posts not found")

        return list(posts)

    async def find_by_user_id(self, limit : int, cursor : str | None, user_id : int, db : AsyncSession) -> List[Post] : 

        statement = select(Post).options(selectinload(Post.user)).where(Post.user_id == user_id).order_by(desc(Post.created_at)).limit(limit=limit + 1)

        if cursor : 
            last_date_str : str = base64.urlsafe_b64decode(cursor.encode()).decode()
            last_date : datetime = datetime.fromisoformat(last_date_str)
            statement = statement.where(Post.created_at < last_date)
           
        result = await db.execute(statement=statement)
        posts = result.scalars().all()

        if not posts : 
            raise NotFound("No post")

        return list(posts)

    async def find_by_id(self, post_id : int, db : AsyncSession) -> Post : 

        statement = select(Post).options(selectinload(Post.user)).where(Post.id == post_id)
        result = await db.execute(statement=statement)
        post = result.scalar_one_or_none()

        if not post : 
            raise NotFound("Post not found")

        return post

    async def create(self, payload : PostRequest, user_id : int, db : AsyncSession) -> Post : 

        post : Post = Post(
            title=payload.title,
            content=payload.content,
            image=payload.image_path,
            user_id=user_id
        )

        db.add(post)
        await db.flush()
        await db.refresh(post)

        return post

    async def delete(self, post_id : int, db : AsyncSession) -> None :

        post : Post = await self.find_by_id(post_id=post_id, db=db)
        await db.delete(post)
        await db.flush()

        return None

    async def update(self, payload : PostUpdate, post_id : int, db : AsyncSession) -> Post : 
        post : Post = await self.find_by_id(post_id=post_id, db=db)

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)

        post.updated_at = datetime.now()

        db.add(post)
        await db.flush()
        await db.refresh(post)

        return post

    async def like(self, post_id : int, db : AsyncSession) -> Post :

        post : Post = await self.find_by_id(post_id=post_id, db=db)

        post.like += 1

        db.add(post)
        await db.flush()
        await db.refresh(post)

        return post

    async def dislike(self, post_id : int, db : AsyncSession) -> Post :

        post : Post = await self.find_by_id(post_id=post_id, db=db)

        post.dislike += 1

        db.add(post)
        await db.flush()
        await db.refresh(post)

        return post
