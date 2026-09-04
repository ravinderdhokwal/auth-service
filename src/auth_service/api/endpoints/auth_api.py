from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.api.deps import get_db_session
from auth_service.schema.user_schema import UserResponse, UserSignInRequest, UserSignUpRequest
from auth_service.services import auth_service
from auth_service.utils.prefixes import AUTH_API_PREFIX


router = APIRouter(prefix=AUTH_API_PREFIX, tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(user_signup_object: UserSignUpRequest, db_session: AsyncSession = Depends(get_db_session)):
    return await auth_service.sign_up(user_signup_object, db_session)

@router.post("/signin", status_code=status.HTTP_200_OK)
async def sign_in(user_signin_object: UserSignInRequest, db_session: AsyncSession = Depends(get_db_session)):
    return await auth_service.sign_in(user_signin_object, db_session)