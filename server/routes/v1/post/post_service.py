from datetime import datetime, timezone
from operator import pos
from routes.v1.post.dto.post_response import PostResponse
from routes.v1.post.dto.post_request import PostRequest
from routes.v1.post.dto.post_update import PostUpdate
from schemas.post import Post
from utils.errors.index import BadRequest
from .post_repository import PostRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pathlib import Path


class PostService : 

    def __init__(self) : 
        self.post_repository = PostRepository()
        self.uploads = Path("uploads")
        self.uploads.mkdir(exist_ok=True)

    async def find_all(self, db : AsyncSession) -> List[PostResponse]: 
        
        posts : List[Post] = await self.post_repository.find_all(db=db)

        response : List[PostResponse] = [
            PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                like=post.like,
                dislike=post.dislike,
                image=post.image,
                user=post.user,
                create_at=post.created_at
            )
            for post in posts
        ]
        await db.commit()
        return response

    async def find_by_user_id(self, user_id : int, db : AsyncSession) -> List[PostResponse] :
        posts : List[Post] = await self.post_repository.find_by_user_id(user_id=user_id, db=db)

        response : List[PostResponse] = [
            PostResponse(

                id=post.id,
                title=post.title,
                content=post.content,
                like=post.like,
                dislike=post.dislike,
                image=post.image,
                user=post.user,
                create_at=post.created_at
            )
            for post in posts
        ]

        return response

    async def find_by_id(self, post_id : int, db : AsyncSession) -> PostResponse : 

        post : Post = await self.post_repository.find_by_id(post_id=post_id, db=db)

        response : PostResponse = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            like=post.like,
            dislike=post.dislike,
            image=post.image,
            user=post.user,
            create_at=post.created_at

        )
        await db.commit()
        return response
    
    async def create(self, payload : PostRequest, user_id : int, db : AsyncSession) -> PostResponse :

        modified_payload : PostRequest = payload
        if payload.image : 

            filename : str = f"{int(datetime.now(timezone.utc).timestamp())}_{payload.image.filename}"
            path = self.uploads / filename

            with open(path, "wb") as f : 
                f.write(await payload.image.read())

            modified_payload : PostRequest = payload.model_copy(update={"image" : None, "image_path" : str(path)})

        post : Post = await self.post_repository.create(payload=modified_payload, user_id=user_id, db=db)

        response : PostResponse = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            like=post.like,
            dislike=post.dislike,
            image=post.image,
            user=post.user,
            create_at=post.created_at

        )

        await db.commit()
        return response

    async def update(self, payload : PostUpdate, post_id : int, db : AsyncSession) -> PostResponse : 

        post : Post = await self.post_repository.update(payload, post_id=post_id, db=db)
        response : PostResponse = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            like=post.like,
            dislike=post.dislike,
            image=post.image,
            user=post.user,
            create_at=post.created_at
        )

        await db.commit()
        return response

    async def delete(self, post_id : int, db : AsyncSession) -> None : 

        await self.post_repository.delete(post_id=post_id, db=db)

        await db.commit()
        return None


    async def like(self, post_id : int, db : AsyncSession) -> PostResponse : 
        post : Post = await self.post_repository.like(post_id=post_id, db=db)

        response : PostResponse = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            like=post.like,
            dislike=post.dislike,
            image=post.image,
            user=post.user,
            create_at=post.created_at
        )

        await db.commit()

        return response 


    async def dislike(self, post_id : int, db : AsyncSession) -> PostResponse : 
        post : Post = await self.post_repository.dislike(post_id=post_id, db=db)

        response : PostResponse = PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            like=post.like,
            dislike=post.dislike,
            image=post.image,
            user=post.user,
            create_at=post.created_at
        )

        await db.commit()

        return response 
