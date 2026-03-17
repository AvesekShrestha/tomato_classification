from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from routes.v1.post.comment.dto.comment_request import CommentRequest
from schemas.comment import Comment
from utils.errors.index import Unauthorized
from .comment_repository import CommentRepository
from routes.v1.post.comment.dto.comment_response import CommentResponse


class CommentService() : 

    def __init__(self) : 
        self.comment_repository = CommentRepository()

    async def find_by_post_id(self, post_id : int, db : AsyncSession) -> List[CommentResponse] : 

        comments : List[Comment] = await self.comment_repository.find_by_post_id(post_id=post_id, db=db)

        response : List[CommentResponse] = [
            CommentResponse(
                id=comment.id,
                content=comment.content,
                like=comment.like,
                dislike=comment.dislike,
                created_at=comment.created_at,
                user=comment.user
            )
            for comment in comments
        ]
        await db.commit()
        return response

    async def find_by_id(self, comment_id : int, db : AsyncSession) -> CommentResponse :

        comment : Comment = await self.comment_repository.find_by_id(comment_id=comment_id, db=db)

        response : CommentResponse = CommentResponse(
            id=comment.id,
            content=comment.content,
            like=comment.like,
            dislike=comment.dislike,
            created_at=comment.created_at,
            user=comment.user
        )

        await db.commit()
        return response

    async def create(self, payload : CommentRequest, post_id : int, user_id : int, db : AsyncSession) -> CommentResponse :
 
        comment : Comment = await self.comment_repository.create(payload=payload, post_id=post_id, user_id=user_id, db=db)

        response : CommentResponse = CommentResponse(
            id=comment.id,
            content=comment.content,
            like=comment.like,
            dislike=comment.dislike,
            created_at=comment.created_at,
        )
        await db.commit()

        return response

    async def delete(self, comment_id : int, user_id : int, db : AsyncSession) -> None : 

        comment : Comment = await self.comment_repository.find_by_id(comment_id=comment_id, db=db)

        if(comment.user_id != user_id) : 
            raise Unauthorized("you don't have acccess to delete the comment")

        await self.comment_repository.delete(comment_id=comment_id, db=db)

        await db.commit()
        return None

    
    async def like(self, comment_id : int, db : AsyncSession) -> CommentResponse : 

        comment : Comment = await self.comment_repository.like(comment_id=comment_id, db=db)

        response : CommentResponse = CommentResponse(
            id=comment.id,
            content=comment.content,
            like=comment.like,
            dislike=comment.dislike,
            created_at=comment.created_at,
            user=comment.user
        )

        await db.commit()

        return response 


    async def dislike(self, comment_id : int, db : AsyncSession) -> CommentResponse : 
        comment : Comment = await self.comment_repository.dislike(comment_id=comment_id, db=db)

        response : CommentResponse = CommentResponse(
            id=comment.id,
            content=comment.content,
            like=comment.like,
            dislike=comment.dislike,
            created_at=comment.created_at,
            user=comment.user
        )

        await db.commit()

        return response
