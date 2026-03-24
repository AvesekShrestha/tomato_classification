from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from config.database.index import get_db
from config.socket.index import SocketManager
from middlewares.auth_middleware import current_user_id, socket_current_user_id
from routes.v1.chat.chat_service import ChatService
from routes.v1.chat.dto.chat_response import ChatResponse
from routes.v1.chat.dto.message_request import MessageRequest
from utils.errors.index import InternalServerError
from utils.response.index import ResponseModel

router = APIRouter()
socket_manager = SocketManager()
chat_service = ChatService(socket_manager)

@router.websocket("/ws")
async def chat(socket : WebSocket, user_id : int = Depends(socket_current_user_id), db : AsyncSession = Depends(get_db)):
    await socket_manager.connect(user_id=user_id, socket=socket)

    try:
        while True:
            data = await socket.receive_json()
            payload : MessageRequest = MessageRequest(**data)
            await chat_service.send_message(payload=payload, user_id=user_id, db=db)

    except WebSocketDisconnect :
        await socket_manager.disconnect(user_id=user_id)

@router.get("/{receiver_id}", response_model=ResponseModel[List[ChatResponse]], response_model_exclude_none=True)
async def get_message(receiver_id : int, limit : int = 10, cursor : str | None = None, user_id : int = Depends(current_user_id), db : AsyncSession = Depends(get_db)) -> ResponseModel[List[ChatResponse]]:

    try : 
        response : ResponseModel[List[ChatResponse]] = await chat_service.get_message(user_id=user_id, receiver_id=receiver_id, limit=limit, cursor=cursor, db=db)
        return response

    except Exception as e:
        error_mesage : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_mesage)



