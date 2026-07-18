from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from jose import JWTError

from sqlalchemy.orm import Session

from database import get_db
from models import User

from security import SECRET_KEY
from security import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    return user


def role_required(roles: list):

    def checker(
        current_user=Depends(
            get_current_user
        )
    ):

        if current_user.role not in roles:

            raise HTTPException(
                status_code=403,
                detail="Permission Denied"
            )

        return current_user

    return checker