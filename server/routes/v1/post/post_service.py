from datetime import datetime, timezone
from operator import pos
from routes.v1.post.dto.post_response import PostResponse
from routes.v1.post.dto.post_request import PostRequest
from routes.v1.post.dto.post_update import PostUpdate
from routes.v1.post.reaction.dto.reaction_request import ReactionRequest
from schemas.post import Post
from schemas.reaction import TargetType
from utils.response.index import Pagination, ResponseModel
from .post_repository import PostRepository
from .reaction.reaction_service import ReactionService 
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pathlib import Path
import base64

class PostService : 

    def __init__(self) : 
        self.post_repository = PostRepository()
        self.reaction_service = ReactionService()
        self.uploads = Path("uploads")
        self.uploads.mkdir(exist_ok=True)

    async def find_all(self, limit : int, cursor : str | None, db : AsyncSession) -> ResponseModel[List[PostResponse]]:
 
        posts : List[Post] = await self.post_repository.find_all(limit=limit, cursor=cursor, db=db)
        has_more : bool = len(posts) > limit

        if has_more :
            last_created_at = posts[limit-1].created_at.isoformat()
            next_cursor = base64.urlsafe_b64encode(last_created_at.encode()).decode()
            posts = posts[:limit]

        else : 
            next_cursor = None

        response : ResponseModel[List[PostResponse]] = ResponseModel(
            success=True,
            data=[
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
            ],
            message="Posts reterived successfully",
            pagination=Pagination(
                next_cursor=next_cursor,
                has_more=has_more
            )
        )
        
        await db.commit()
        return response

    async def find_by_user_id(self, limit : int, cursor : str | None, user_id : int,  db : AsyncSession) -> ResponseModel[List[PostResponse]] :

        posts : List[Post] = await self.post_repository.find_by_user_id(limit=limit, cursor=cursor, user_id=user_id, db=db)

        has_more : bool = len(posts) > limit

        if has_more :
            last_created_at = posts[limit-1].created_at.isoformat()
            next_cursor = base64.urlsafe_b64encode(last_created_at.encode()).decode()
            posts = posts[:limit]

        else : 
            next_cursor = None

        response : ResponseModel[List[PostResponse]] = ResponseModel(
            success=True,
            data=[
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
            ],
            message="Post reterived successfully",
            pagination=Pagination(
                next_cursor=next_cursor,
                has_more=has_more
            )
        )
        return response

    async def find_by_id(self, post_id : int, db : AsyncSession) -> ResponseModel[PostResponse] : 

        post : Post = await self.post_repository.find_by_id(post_id=post_id, db=db)

        response : ResponseModel[PostResponse] = ResponseModel(
            success=True,
            data=PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                like=post.like,
                dislike=post.dislike,
                image=post.image,
                user=post.user,
                create_at=post.created_at
            ),
            message="Post data retrived successfully"
        )

        await db.commit()
        return response
    
    async def create(self, payload : PostRequest, user_id : int, db : AsyncSession) -> ResponseModel[PostResponse] :

        modified_payload : PostRequest = payload
        if payload.image :

            filename : str = f"{int(datetime.now(timezone.utc).timestamp())}_{payload.image.filename}"
            path = self.uploads / filename

            with open(path, "wb") as f : 
                f.write(await payload.image.read())

            modified_payload : PostRequest = payload.model_copy(update={"image" : None, "image_path" : str(path)})

        post : Post = await self.post_repository.create(payload=modified_payload, user_id=user_id, db=db)

        response : ResponseModel[PostResponse] = ResponseModel(
            success=True,
            data=PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                like=post.like,
                dislike=post.dislike,
                image=post.image,
                create_at=post.created_at
            ),
            message="post created successfully"
        )

        await db.commit()
        return response

    async def update(self, payload : PostUpdate, post_id : int, db : AsyncSession) -> ResponseModel[PostResponse] : 

        post : Post = await self.post_repository.update(payload, post_id=post_id, db=db)
        response : ResponseModel[PostResponse] = ResponseModel(
            success=True,
            data=PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                like=post.like,
                dislike=post.dislike,
                image=post.image,
                user=post.user,
                create_at=post.created_at
            ),
            message="Post updated successfully"
        )

        await db.commit()
        return response

    async def delete(self, post_id : int, db : AsyncSession) -> ResponseModel[None] : 

        await self.post_repository.delete(post_id=post_id, db=db)

        await db.commit()
        return ResponseModel(
            success=True,
            data=None,
            message="Post deleted successfully"
        )

    async def like(self, post_id : int, user_id : int, db : AsyncSession) -> ResponseModel[PostResponse] : 

        payload : ReactionRequest = ReactionRequest(
            is_like=True,
            target_id=post_id,
            target_type=TargetType.POST
        )
        post : ResponseModel[PostResponse] = await self.reaction_service.toggle_post_reaction(payload=payload, user_id=user_id, db=db)

        await db.commit()
        return post 

    async def dislike(self, post_id : int, user_id : int, db : AsyncSession) -> ResponseModel[PostResponse] : 

        payload : ReactionRequest = ReactionRequest(
            is_like=False,
            target_id=post_id,
            target_type=TargetType.POST
        )
        post : ResponseModel[PostResponse] = await self.reaction_service.toggle_post_reaction(payload=payload, user_id=user_id, db=db)

        await db.commit()
        return post 
