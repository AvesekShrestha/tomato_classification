import base64
from datetime import datetime
from typing import List
from sqlalchemy import desc, select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from routes.v1.chat.dto.chat_request import ChatRequest
from schemas.chat import Chat
from utils.errors.index import NotFound


class ChatRepository : 

    async def create(self, payload : ChatRequest, db : AsyncSession) -> Chat :

        chat : Chat = Chat(
            message=payload.message,
            sender_id=payload.sender_id,
            receiver_id=payload.receiver_id,
            is_read=payload.is_read,
            messaged_at=payload.messaged_at
        )

        db.add(chat)
        await db.flush()
        await db.refresh(chat)

        return chat

    async def get_message(self, user_id : int, receiver_id : int, limit : int, cursor : str | None, db : AsyncSession) -> List[Chat] :

        statement = select(Chat).where(
            or_(
                and_(Chat.sender_id == user_id, Chat.receiver_id == receiver_id),
                and_(Chat.sender_id == receiver_id, Chat.receiver_id == user_id)
            )
        ).order_by(desc(Chat.messaged_at)).limit(limit + 1)
        if cursor : 
            last_messaged_date_str : str = base64.urlsafe_b64decode(cursor.encode()).decode()
            last_messaged_date : datetime = datetime.fromisoformat(last_messaged_date_str)
            statement = statement.where(Chat.messaged_at < last_messaged_date)

        result = await db.execute(statement=statement)
        chats = result.scalars().all()

        return list(chats)


    async def get_user_messages(self, user_id: int, db : AsyncSession) -> List[Chat]:
        result = await db.execute(
            select(Chat)
            .where(
                or_(
                    Chat.sender_id == user_id,
                    Chat.receiver_id == user_id,
                )
            )
            .order_by(Chat.messaged_at.desc())
        )

        return list(result.scalars().all())
