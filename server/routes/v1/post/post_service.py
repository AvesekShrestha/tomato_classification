from routes.v1.post.dto.post_response import PostResponse
from routes.v1.post.dto.post_request import PostRequest
from schemas.post import Post
from .post_repository import PostRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class PostService : 

    def __init__(self) : 
        self.post_repository = PostRepository()

    async def find_all(self, db : AsyncSession) -> List[PostResponse]: 
        
        posts : List[Post] = await self.post_repository.find_all(db=db)

        response : List[PostResponse] = [
            PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                like=post.like,
                dislike=post.dislike
            )
            for post in posts
        ]
        await db.commit()
        return response

    async def find_by_id(self, post_id : int, db : AsyncSession) -> PostResponse : 

        post : Post = await self.post_repository.find_by_id(post_id=post_id, db=db)

        response : PostResponse = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            like=post.like,
            dislike=post.dislike
        )
        await db.commit()
        return response
    
    async def create(self, payload : PostRequest, user_id : int, db : AsyncSession) -> PostResponse :

        post : Post = await self.post_repository.create(payload=payload, user_id=user_id, db=db)

        response : PostResponse = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            like=post.like,
            dislike=post.dislike
        )

        await db.commit()
        return response

    async def delete(self, post_id : int, db : AsyncSession) -> None : 

        await self.post_repository.delete(post_id=post_id, db=db)

        await db.commit()
        return None


