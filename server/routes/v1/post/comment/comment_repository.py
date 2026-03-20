from sqlalchemy import select
from sqlalchemy.engine import result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import datetime
from typing import List
from routes.v1.post.comment.dto.comment_request import CommentRequest
from schemas.comment import Comment
from utils.errors.index import NotFound


class CommentRepository : 

    async def find_by_post_id(self, post_id : int, db : AsyncSession) -> List[Comment]:
 
        statement = select(Comment).options(selectinload(Comment.user)).where(Comment.post_id == post_id, Comment.parent_id == None)
        result = await db.execute(statement=statement)
        comments = result.scalars().all()

        if not comments : 
            raise NotFound("No comments found")

        return list(comments) 

    async def find_by_id(self, comment_id : int, db : AsyncSession) -> Comment : 
        
        statement = select(Comment).options(selectinload(Comment.user)).where(Comment.id == comment_id)
        result = await db.execute(statement=statement)
        comment = result.scalar_one_or_none()

        if not comment :
            raise NotFound("No such comment")

        return comment

    async def create(self, payload : CommentRequest, post_id : int, user_id : int, db : AsyncSession) -> Comment : 

        comment : Comment = Comment(
            content=payload.content,
            user_id=user_id,
            post_id=post_id,
            updated_at=datetime.now()
        )

        db.add(comment)
        await db.flush()
        await db.refresh(comment)
        
        return comment

    async def delete(self, comment_id : int, db : AsyncSession) -> None :

        comment = await self.find_by_id(comment_id=comment_id, db=db)
        await db.delete(comment)
        await db.flush()

        return None

    async def like(self, comment_id : int, db : AsyncSession) -> Comment :

        comment : Comment = await self.find_by_id(comment_id=comment_id, db=db)

        comment.like += 1

        db.add(comment)
        await db.flush()
        await db.refresh(comment)

        return comment 

    async def dislike(self, comment_id : int, db : AsyncSession) -> Comment :

        comment : Comment = await self.find_by_id(comment_id=comment_id, db=db)

        comment.dislike += 1

        db.add(comment)
        await db.flush()
        await db.refresh(comment)

        return comment 

    async def reply(self, payload : CommentRequest, post_id : int, comment_id : int, user_id : int, db : AsyncSession) -> Comment :

        reply : Comment = Comment(
            content=payload.content,
            user_id=user_id,
            post_id=post_id,
            parent_id=comment_id,
            updated_at=datetime.now()
        )

        db.add(reply)
        await db.flush()
        await db.refresh(reply)

        return reply

    async def get_reply(self, comment_id : int, db : AsyncSession) -> List[Comment] :

        statement = select(Comment).options(selectinload(Comment.replies)).where(Comment.parent_id == comment_id)
        result = await db.execute(statement=statement)
        replies = result.scalars().all()

        if not replies : 
            raise NotFound("No replies")

        return list(replies)

