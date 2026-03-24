import base64
from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from config.socket.index import SocketManager
from routes.v1.chat.dto.chat_request import ChatRequest
from routes.v1.chat.dto.chat_response import ChatResponse
from routes.v1.chat.dto.message_request import MessageRequest
from schemas.chat import Chat
from .chat_repository import ChatRepository
from utils.response.index import Pagination, ResponseModel

class ChatService: 

    def __init__(self, manager : SocketManager) : 
        self.socket_manager = manager
        self.chat_repository = ChatRepository()

    async def send_message(self, payload : MessageRequest, user_id : int, db : AsyncSession) :
        await self.socket_manager.send_message(to=payload.to, message=payload.message)

        chat_payload : ChatRequest = ChatRequest(
            message=payload.message,
            sender_id=user_id,
            receiver_id=payload.to,
            is_read=False,
            messaged_at=datetime.now()
        )

        await self.chat_repository.create(payload=chat_payload, db=db)
        await db.commit()


    async def get_message(self, user_id : int, receiver_id : int, limit : int, cursor : str | None, db : AsyncSession) -> ResponseModel[List[ChatResponse]] :

        chats : List[Chat] = await self.chat_repository.get_message(user_id=user_id, receiver_id=receiver_id, limit=limit, cursor=cursor, db=db)
        has_more : bool = len(chats) > limit

        if has_more : 
            last_messaged_at = chats[limit-1].messaged_at.isoformat()
            next_cursor = base64.urlsafe_b64encode(last_messaged_at.encode()).decode()
            chats = chats[:limit]

        else : 
            next_cursor = None

        response : ResponseModel[List[ChatResponse]] = ResponseModel(
            success=True,
            data=[
                ChatResponse(
                    message=chat.message,
                    sender_id=chat.sender_id,
                    receiver_id=chat.receiver_id,
                    is_read=chat.is_read,
                    messaged_at=chat.messaged_at
                )
                for chat in chats
            ],
            message="Chat reterived successfully",
            pagination=Pagination(
                next_cursor=next_cursor,
                has_more=has_more
            )
        )
        return response
