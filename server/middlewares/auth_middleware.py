from fastapi import Request
from utils.errors.index import Unauthorized
from utils.tokens.token_type import AccessTokenPayload
from utils.tokens.index import decode_access_token


def authenticate(request : Request) -> int : 

    try : 
        access_token = request.cookies.get("accessToken")

        if not access_token : 
            raise Unauthorized("Access token is not present")

        user : AccessTokenPayload = decode_access_token(access_token)
        return user.user_id

    except Exception as e: 
        raise e
