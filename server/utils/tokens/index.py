import jwt
from utils.tokens.token_type import AccessTokenPayload, RefreshTokenPayload
from config.constants.index import jwt_private_key

def generate_access_token(payload : AccessTokenPayload) -> str : 
    encoded = jwt.encode(payload.model_dump(), jwt_private_key, algorithm="RS256")
    return encoded

def generate_refresh_token(payload : RefreshTokenPayload) -> str : 
    encoded = jwt.encode(payload.model_dump(), jwt_private_key, algorithm="RS256")
    return encoded

def decode_access_token(token : str) -> AccessTokenPayload:
    decoded = jwt.decode(token, jwt_private_key, algorithms=["RS256"])
    return AccessTokenPayload.model_validate(decoded)

def decode_refresh_token(token : str) -> RefreshTokenPayload:
    decoded = jwt.decode(token, jwt_private_key, algorithms=["RS256"])
    return RefreshTokenPayload.model_validate(decoded)
