from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth_service.core import security
from auth_service.models import UserModel
from auth_service.schema.user_schema import UserSignUpRequest


async def save_user(user_signup_object: UserSignUpRequest, db_session: AsyncSession) -> UserModel:
    user = UserModel(
        full_name = user_signup_object.full_name,
        email = user_signup_object.email,
        hashed_password = security.hash_password(user_signup_object.password)
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    return user

async def get_user_by_email(email: str, db_session: AsyncSession) -> UserModel:
    user = await db_session.execute(select(UserModel).where(UserModel.email == email))
    return user.scalar_one_or_none()