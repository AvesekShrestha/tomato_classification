import jwt
from utils.errors.index import InternalServerError
from utils.tokens.token_type import AccessTokenPayload 
from config.constants.index import jwt_private_key
import secrets

def generate_access_token(payload : AccessTokenPayload) -> str : 
    encoded = jwt.encode(payload.model_dump(), jwt_private_key, algorithm="HS256")
    return encoded

def decode_access_token(token : str) -> AccessTokenPayload:
    print("Calling here")
    try : 
        decoded = jwt.decode(token, jwt_private_key, algorithms=["HS256"])
        return AccessTokenPayload.model_validate(decoded)
    except Exception as e : 
        raise InternalServerError(e.args[0])

def generate_refresh_token() : 
    return secrets.token_urlsafe(64)
