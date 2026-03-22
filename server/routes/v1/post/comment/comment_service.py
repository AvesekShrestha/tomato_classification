from typing import List
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from routes.v1.post.comment.dto.comment_request import CommentRequest
from routes.v1.post.reaction.dto.reaction_request import ReactionRequest
from schemas.comment import Comment
from schemas.reaction import TargetType
from utils.errors.index import Unauthorized
from utils.response.index import Pagination, ResponseModel
from .comment_repository import CommentRepository
from routes.v1.post.comment.dto.comment_response import CommentResponse
from routes.v1.post.reaction.reaction_service import ReactionService 
import base64


class CommentService() : 

    def __init__(self) : 
        self.comment_repository = CommentRepository()
        self.reaction_service = ReactionService()

    async def find_by_post_id(self, post_id : int, limit : int, cursor : str | None, db : AsyncSession) -> ResponseModel[List[CommentResponse]] : 

        comments : List[Comment] = await self.comment_repository.find_by_post_id(post_id=post_id, limit=limit, cursor=cursor, db=db)

        has_more : bool = len(comments) > limit

        if has_more : 
            last_created_at = comments[limit-1].created_at.isoformat()
            next_cursor = base64.urlsafe_b64encode(last_created_at.encode()).decode()
            comments = comments[:limit]
        else : 
            next_cursor = None

        response : ResponseModel[List[CommentResponse]] = ResponseModel(
            success=True,
            data=[
                CommentResponse(
                    id=comment.id,
                    content=comment.content,
                    like=comment.like,
                    dislike=comment.dislike,
                    created_at=comment.created_at,
                    user=comment.user,
                )
                for comment in comments
            ],
            message="Comment reterived successfully",
            pagination=Pagination(
                next_cursor=next_cursor,
                has_more=has_more
            )
        )
        
        await db.commit()
        return response

    async def find_by_id(self, comment_id : int, db : AsyncSession) -> ResponseModel[CommentResponse] :

        comment : Comment = await self.comment_repository.find_by_id(comment_id=comment_id, db=db)

        response : ResponseModel[CommentResponse] = ResponseModel(
            success=True,
            data=CommentResponse(
                id=comment.id,
                content=comment.content,
                like=comment.like,
                dislike=comment.dislike,
                created_at=comment.created_at,
                user=comment.user
            ),
            message="Comment reterived successfully"
        )

        await db.commit()
        return response

    async def create(self, payload : CommentRequest, post_id : int, user_id : int, db : AsyncSession) -> ResponseModel[CommentResponse] :
 
        comment : Comment = await self.comment_repository.create(payload=payload, post_id=post_id, user_id=user_id, db=db)

        response : ResponseModel[CommentResponse] = ResponseModel(
            success=True,
            data=CommentResponse(
                id=comment.id,
                content=comment.content,
                like=comment.like,
                dislike=comment.dislike,
                created_at=comment.created_at,
            ),
            message="Comment created successfully"
        )

        await db.commit()
        return response

    async def get_reply(self, comment_id : int, limit : int, cursor : str | None, db : AsyncSession) -> ResponseModel[List[CommentResponse]] :

        replies : List[Comment] = await self.comment_repository.get_reply(comment_id=comment_id, limit=limit, cursor=cursor, db=db)
        has_more : bool = len(replies) > limit

        if has_more : 
            last_created_at = replies[limit-1].created_at.isoformat()
            next_cursor = base64.urlsafe_b64encode(last_created_at.encode()).decode()
            replies = replies[:limit]
        else : 
            next_cursor = None

        response : ResponseModel[List[CommentResponse]] = ResponseModel(
            success=True,
            data=[
                CommentResponse(
                    id=reply.id,
                    content=reply.content,
                    like=reply.like,
                    dislike=reply.dislike,
                    created_at=reply.created_at,
                ) for reply in replies
            ],
            message="replies reterived successfully",
            pagination=Pagination(
                next_cursor=next_cursor,
                has_more=has_more
            )
        )
        return response

    async def reply(self, payload : CommentRequest, post_id : int, comment_id : int, user_id : int, db : AsyncSession) -> ResponseModel[CommentResponse] : 

        reply : Comment = await self.comment_repository.reply(payload=payload, post_id=post_id, comment_id=comment_id, user_id=user_id, db=db)

        response : ResponseModel[CommentResponse] = ResponseModel(
            success=True,
            data=CommentResponse(
                id=reply.id,
                content=reply.content,
                like=reply.like,
                dislike=reply.dislike,
                created_at=reply.created_at,
            ),
            message="Reply created successfully"
        )

        await db.commit()
        return response

    async def delete(self, comment_id : int, user_id : int, db : AsyncSession) -> ResponseModel[None] : 

        comment : Comment = await self.comment_repository.find_by_id(comment_id=comment_id, db=db)

        if(comment.user_id != user_id) : 
            raise Unauthorized("you don't have acccess to delete the comment")

        await self.comment_repository.delete(comment_id=comment_id, db=db)

        await db.commit()
        return ResponseModel[None](
            success=True,
            data=None,
            message="Comment deleted successfully"
        )

    async def like(self, user_id : int, comment_id : int, db : AsyncSession) -> ResponseModel[CommentResponse] : 

        payload : ReactionRequest = ReactionRequest(
            is_like=True,
            target_id=comment_id,
            target_type=TargetType.COMMENT
        )
        comment : ResponseModel[CommentResponse] = await self.reaction_service.toggle_comment_reaction(payload=payload, user_id=user_id, db=db)

        await db.commit()
        return comment 

    async def dislike(self, comment_id : int, user_id : int, db : AsyncSession) -> ResponseModel[CommentResponse] : 
        payload : ReactionRequest = ReactionRequest(
            is_like=False,
            target_id=comment_id,
            target_type=TargetType.COMMENT
        )
        comment : ResponseModel[CommentResponse] = await self.reaction_service.toggle_comment_reaction(payload=payload, user_id=user_id, db=db)

        await db.commit()
        return comment 
