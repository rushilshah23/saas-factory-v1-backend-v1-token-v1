from dotenv import load_dotenv
import os
load_dotenv()


class Config:
    JWT_SECRET_KEY:str = os.environ['JWT_SECRET_KEY']
    JWT_ACCESS_TOKEN_EXPIRY:int = int(os.environ['JWT_ACCESS_TOKEN_EXPIRY'])
    JWT_ALGORITHM:str = os.environ['JWT_ALGORITHM']
    COOKIE_ACCESS_TOKEN_KEY:str = 'access_key'
    COOKIE_HTTP_ONLY:bool=True
    COOKIE_SECURE:bool=True         # Use HTTPS only
    COOKIE_SAMESITE:str="Strict"   # Prevent CSRF (can be Lax depending on app)
