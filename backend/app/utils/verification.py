from itsdangerous import URLSafeTimedSerializer
from app.config import Config
from app.core.logger import logger

serialiser = URLSafeTimedSerializer(
    secret_key=Config.SECRET_KEY,
    salt="email=configuration"

)
def createUrlSafeToken(data: dict):
    # itsdangerous.URLSafeTimedSerializer is called “Timed” you don’t need to manually assign a timestamp when creating the token. It automatically adds a timestamp internally when you call dumps().
    token = serialiser.dumps(data)
    return token


def decodeUrlSafeToken(token: str, max_age: int = 86400):
    try:
        tokenData = serialiser.loads(token, max_age)  # token valid for 1 hour
        return tokenData
    except Exception as e:
        logger("Decoder Url Error: ", exc_info=True)
        raise

