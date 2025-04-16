import os
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from auth import oauth2_scheme
from dotenv import load_dotenv
from services.user import user_service
from schemas.user import User

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')  
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # print("DEBUG:: raw token:", token)
        # print("DEBUG:: using secret:", SECRET_KEY)
        # print("DEBUG:: algorithm:", ALGORITHM)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("DEBUG:: payload:", payload)

        email: str = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="not email")
    except JWTError as e:
        print("JWTError:", e)
        raise HTTPException(status_code=401, detail="jwt error")

    user = user_service.get_user_by_email(email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="none")
    
    return User(**user.model_dump())