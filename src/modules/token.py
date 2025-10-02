import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from src.common.utils.logger import get_logger

logger = get_logger(__name__)

class TokenManagement:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expiry_minutes: int = 60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiry_minutes = expiry_minutes
        



    def generate_token(self, data: Dict) -> str:
        try:
            payload = data.copy()
            # Use timezone-aware UTC datetime
            payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=self.expiry_minutes)
            return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            logger.error("Invalid payload - ", e)
            return None

    def validate_token(self, token: str) -> Optional[Dict]:
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired.")
        except jwt.InvalidTokenError:
            logger.error("Invalid token.")
        return None
