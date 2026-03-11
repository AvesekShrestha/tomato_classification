from fastapi import Request
from utils.errors.index import BadRequest, InternalServerError
from utils.tokens.index import decode_access_token
from utils.tokens.token_type import AccessTokenPayload


def authenticate(request : Request) -> int : 

    try : 
        auth_header = request.headers.get("authorization")

        if not auth_header : 
            raise BadRequest("Access token is not present")
    
        access_token : str = auth_header.split(" ")[1]

        user : AccessTokenPayload = decode_access_token(access_token)

        return user.user_id

    except Exception as e: 

        error_message : str = e.args[0] if e.args[0] else str(e)
        raise InternalServerError(error_message)
