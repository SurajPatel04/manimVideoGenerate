from itsdangerous import URLSafeTimedSerializer
from app.config.config import Config
from app.core.logger import logger

serialiser = URLSafeTimedSerializer(
    secret_key=Config.SECRET_KEY,
    salt="email=configuration"

)
def createUrlSafeToken(data: dict):
    token = serialiser.dumps(data)
    return token


def decodeUrlSafeToken(token: str, max_age: int = 86400):
    try:
        tokenData = serialiser.loads(token, max_age)
        return tokenData
    except Exception as e:
        logger("Decoder Url Error: ", exc_info=True)
        raise

