from routes.v1.post.dto.post_request import PostRequest
from schemas.post import Post
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from utils.errors.index import NotFound

class PostRepository : 

    def __init__(self) : 
        pass

    async def find_all(self, db : AsyncSession) -> List[Post] : 

        statement = select(Post)
        result = await db.execute(statement=statement)
        posts = result.scalars()._allrows()

        if not posts : 

            raise NotFound("Posts not found")

        return posts

    async def find_by_id(self, post_id : int, db : AsyncSession) -> Post : 

        statement = select(Post).where(Post.id == post_id)
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
