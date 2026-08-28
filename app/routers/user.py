from fastapi import APIRouter, HTTPException, Depends
from app.config.database import get_db
from app.config.config import hash_password, verify_password, encode_access_token
from app.model.models import User
from app.schema.schemas import UserProfileResponse, UserRegistrationRequest, UserLoginResponse, UserLoginRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from app.depends.auth_depends import require_user_id


router = APIRouter()

@router.post("/register", response_model=UserProfileResponse)
async def register(request: UserRegistrationRequest, db: AsyncSession=Depends(get_db)):
    
    new_user = User(
        first_name = request.first_name.strip(),
        last_name = request.last_name.strip(),
        email = request.email.strip().lower(),
        phone = request.phone.strip(),
        password = hash_password(request.password)
    )
    
    db.add(new_user)
    
    try:
        await db.commit()
        await db.refresh(new_user)
    except:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Internal Server Error")
    
    return UserProfileResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        phone=new_user.phone,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
    )
    
    
    
    
@router.post("/login", response_model=UserLoginResponse)
async def login(request: UserLoginRequest, db: AsyncSession=Depends(get_db)):
    email = request.email.strip().lower()
    password = request.password
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is not None and verify_password(password, user.password):
        return UserLoginResponse(
            access_token= encode_access_token(user.id, user.email)
        )
    
    raise HTTPException(status_code=401, detail="Incorrect email or password")



# Protected routes - After login
@router.get("/profile", response_model=UserProfileResponse)
async def profile(user_id: Annotated[int, Depends(require_user_id)], db: AsyncSession=Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is not None:
        return UserProfileResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
    raise HTTPException(status_code=401, detail="User not found!")