from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import User
from src.schemas.token import TokenPayload
from src.services.auth import AuthService
from src.utils import ALGORITHM, JWT_SECRET_KEY

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/swagger/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = AuthService.get_user_by_id(user_id=token_data.sub, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


async def get_admin(user: User = Depends(get_current_user)):
    if user.is_admin:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to access this resource",
        headers={"WWW-Authenticate": "Bearer"},
    )
