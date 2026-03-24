from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.post import Post
from schemas.reaction import Reaction, TargetType
from schemas.comment import Comment
from routes.v1.post.reaction.dto.reaction_request import ReactionRequest


class ReactionRepository : 

    async def find(self, user_id : int, target_id : int, target_type : TargetType, db : AsyncSession) -> Reaction | None:

        statement = select(Reaction).where(Reaction.target_id == target_id, Reaction.user_id == user_id, Reaction.target_type == target_type)
        result = await db.execute(statement=statement)
        reaction = result.scalar_one_or_none()

        return reaction

    async def toggle_reaction(self, payload : ReactionRequest, user_id : int, target : Post | Comment , db : AsyncSession) -> Post | Comment: 

        existing = await self.find(user_id=user_id, target_id=payload.target_id, target_type=payload.target_type, db=db)

        if not existing:
            reaction = Reaction(
                user_id=user_id,
                target_id=payload.target_id,
                target_type=payload.target_type,
                is_like=payload.is_like
            )
            if(payload.is_like) : 
                target.like += 1
            else :
                target.dislike += 1

            db.add(reaction)
            await db.flush()
            await db.refresh(target)
            return target

        if existing.is_like == payload.is_like:

            if payload.is_like : 
                target.like = max(target.like - 1, 0)
            else :
                target.dislike = max(target.dislike - 1, 0)

            await db.delete(existing)
            await db.flush()
            await db.refresh(target)
            return target
           

        existing.is_like = payload.is_like

        if payload.is_like :
            target.like += 1
            target.dislike = max(target.dislike - 1, 0)
        else :
            target.dislike += 1
            target.like = max(target.like - 1, 0)

        await db.flush()
        await db.refresh(target)
        return target
