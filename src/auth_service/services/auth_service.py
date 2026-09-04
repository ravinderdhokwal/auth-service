from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.core.exceptions import AlreadyExistsError
from auth_service.repo import user_repo
from auth_service.schema.user_schema import UserResponse, UserSignInRequest, UserSignUpRequest
from auth_service.utils import message


async def sign_up(user_signup_object: UserSignUpRequest, db_session: AsyncSession):
    user = await user_repo.get_user_by_email(user_signup_object.email, db_session)

    if user:
        raise AlreadyExistsError(
            message.USER_ALREADY_EXISTS, 
            data=UserResponse(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        )
    
    return await user_repo.save_user(user_signup_object, db_session)

async def sign_in(user_signin_object: UserSignInRequest, db_session: AsyncSession):
    pass