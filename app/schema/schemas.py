from pydantic import BaseModel, EmailStr
from datetime import datetime

 
# User Registration Request    
class UserRegistrationRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str

# User Login Request
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    

# User Login Response    
class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str="bearer"
    
    
# User Profile Response
class UserProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime