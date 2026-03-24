from fastapi import Request, WebSocket, WebSocketException
from utils.errors.index import Unauthorized
from utils.tokens.token_type import AccessTokenPayload
from utils.tokens.index import decode_access_token

async def socket_current_user_id(socket: WebSocket) -> int:
    access_token = socket.cookies.get("accessToken")
    if not access_token:
        await socket.close(code=1008)
        raise WebSocketException(code=1008, reason="Unauthorized")
    
    try:
        user: AccessTokenPayload = decode_access_token(access_token)
        return user.user_id
    except Exception:
        await socket.close(code=1008)
        raise WebSocketException(code=1008, reason="Invalid token")

def current_user_id(request : Request) -> int : 

    try : 
        access_token = request.cookies.get("accessToken")

        if not access_token : 
            raise Unauthorized("Access token is not present")

        user : AccessTokenPayload = decode_access_token(access_token)
        return user.user_id

    except Exception as e: 
        raise e

def authenticate(request : Request) -> None : 

    try :
        access_token = request.cookies.get("accessToken")

        if not access_token : 
            raise Unauthorized("Access token is not present")

        decode_access_token(access_token)

    except Exception as e: 
        raise e

