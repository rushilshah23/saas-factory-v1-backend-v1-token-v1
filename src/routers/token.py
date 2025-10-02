from fastapi import APIRouter, Request, Response, Depends, Header, Cookie
from src.modules.token import TokenManagement
from src.config import Config
from src.common.helpers.response import CustomResponse
from src.common.helpers.status_codes import StatusCodes
from src.helpers.token import Token
from typing import Optional


router = APIRouter(prefix="/token")


token_management = TokenManagement(
    secret_key=Config.JWT_SECRET_KEY,
    expiry_minutes=Config.JWT_ACCESS_TOKEN_EXPIRY
)


@router.post("/generate")
async def generate_token(request:Request, response:Response):
    body = await request.json()
    token_data = body.get("token_data")
    generated_token = token_management.generate_token(token_data)
    if generated_token is None:
        return CustomResponse(status_code=StatusCodes.HTTP_400_BAD_REQUEST,message="Invalid payload").to_dict()
    token = Token(access_token=generated_token, refresh_token=None)

    # Set the geenrate token in cookies for web along with returning as well so mobile apps can use it. 
    response.set_cookie(
        key="access_token",
        value=generated_token,
        httponly=Config.COOKIE_HTTP_ONLY,
        secure=Config.COOKIE_SECURE,         # Use HTTPS only
        samesite=Config.COOKIE_SAMESITE,   # Prevent CSRF (can be Lax depending on app)
        max_age=Config.JWT_ACCESS_TOKEN_EXPIRY
    )
    return CustomResponse(status_code=StatusCodes.HTTP_201_CREATED,message="Token generated successfully", data=token.to_dict()).to_dict()


@router.post("/validate")
async def validate_token(request:Request):
    request_cookies = request.cookies
    request_headers = request.headers

    authorization = request_headers.get("Authorization")
    access_token_cookie = request_cookies.get("access_token")
    # GET TOKEN FROM COOKIE FOR WEB ELSE IF APP FROM AUTHORIZATION HEADER
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]  # From mobile app/API client
    elif access_token_cookie:
        token = access_token_cookie           # From browser cookie

    if not token:
        return CustomResponse(
            status_code=StatusCodes.HTTP_401_UNAUTHORIZED,
            message="No token provided"
        ).to_dict()
    token_data = token_management.validate_token(token=token)
    if token_data is None:
        return CustomResponse(status_code=StatusCodes.HTTP_401_UNAUTHORIZED,message="Invalid or expired token").to_dict()
    return CustomResponse(status_code=StatusCodes.HTTP_200_OK, message="Valid token", data=token_data)



