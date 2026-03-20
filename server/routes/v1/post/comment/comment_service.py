from operator import is_
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user

from routes.v1.post.comment.dto.comment_request import CommentRequest
from routes.v1.post.reaction.dto.reaction_request import ReactionRequest
from schemas.comment import Comment
from schemas.reaction import TargetType
from utils.errors.index import Unauthorized
from .comment_repository import CommentRepository
from routes.v1.post.comment.dto.comment_response import CommentResponse
from routes.v1.post.reaction.reaction_service import ReactionService 


class CommentService() : 

    def __init__(self) : 
        self.comment_repository = CommentRepository()
        self.reaction_service = ReactionService()

    async def find_by_post_id(self, post_id : int, db : AsyncSession) -> List[CommentResponse] : 

        comments : List[Comment] = await self.comment_repository.find_by_post_id(post_id=post_id, db=db)

        response : List[CommentResponse] = [
            CommentResponse(
                id=comment.id,
                content=comment.content,
                like=comment.like,
                dislike=comment.dislike,
                created_at=comment.created_at,
                user=comment.user,
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

    async def get_reply(self, comment_id : int, db : AsyncSession) -> List[CommentResponse] :

        replies : List[Comment] = await self.comment_repository.get_reply(comment_id=comment_id, db=db)

        response : List[CommentResponse] = [
            CommentResponse(
                id=reply.id,
                content=reply.content,
                like=reply.like,
                dislike=reply.dislike,
                created_at=reply.created_at,
            ) for reply in replies
        ]

        return response

    async def reply(self, payload : CommentRequest, post_id : int, comment_id : int, user_id : int, db : AsyncSession) -> CommentResponse : 

        reply : Comment = await self.comment_repository.reply(payload=payload, post_id=post_id, comment_id=comment_id, user_id=user_id, db=db)

        response : CommentResponse = CommentResponse(
            id=reply.id,
            content=reply.content,
            like=reply.like,
            dislike=reply.dislike,
            created_at=reply.created_at,
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

    
    async def like(self, user_id : int, comment_id : int, db : AsyncSession) -> CommentResponse : 

        payload : ReactionRequest = ReactionRequest(
            is_like=True,
            target_id=comment_id,
            target_type=TargetType.COMMENT
        )
        comment : CommentResponse = await self.reaction_service.toggle_comment_reaction(payload=payload, user_id=user_id, db=db)
        await db.commit()

        return comment

    async def dislike(self, comment_id : int, user_id : int, db : AsyncSession) -> CommentResponse : 
        payload : ReactionRequest = ReactionRequest(
            is_like=False,
            target_id=comment_id,
            target_type=TargetType.COMMENT
        )
        comment : CommentResponse = await self.reaction_service.toggle_comment_reaction(payload=payload, user_id=user_id, db=db)
        await db.commit()

        return comment

