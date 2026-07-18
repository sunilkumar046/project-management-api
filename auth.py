from jose import jwt
from jose import JWTError

from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models import User

from security import SECRET_KEY
from security import ALGORITHM


def get_current_user(
    token: str,
    db: Session
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