from itsdangerous import URLSafeTimedSerializer
from app.config import Config
from app.core.logger import logger

serialiser = URLSafeTimedSerializer(
    secret_key=Config.SECRET_KEY,
    salt="email=configuration"

)
def createUrlSafeToken(data: dict):
    token = serialiser.dumps(data,)
    return token


def decodeUrlSafeToken(token: dict):
    try:
        tokenData = serialiser.loads(token)
        return tokenData
    
    except Exception as e:
        logger("Decoder Url Error: ", exc_info=True)
