from pydantic import BaseModel, field_validator, Field, EmailStr, HttpUrl, AnyHttpUrl, IPvAnyAddress, FilePath, DirectoryPath
from decimal import Decimal
from typing import Optional, List, Set, Tuple
from enum import Enum


class UnitEnum(str, Enum):
    kg="kg"
    pcs="pcs"

    
class ProductCreate(BaseModel):
    # user_id: int=Field(gt=0)
    user_id: int
    # category_id: int=Field(gt=0)
    category_id: int
    # name: str = Field(min_length=3, max_length=100)
    name: str
    price: Decimal=Field(gt=0, max_digits=6, decimal_places=2)
    # price: float=Field(gt=0)
    unit: UnitEnum
    img_url: Optional[str] | None = None
    # demo: float=Field(gt=0, ge=1, lt=1000, le=999)
    # demo2: int=Field(multiple_of=5)
    # demo3: str = Field(pattern="^[^\s@]+@[^\s@]+\.[^\s@]+$")
    # demo4: Decimal = Field(max_digits=6, decimal_places=2)
    # demo5: Optional[Decimal] = Field(max_digits=3, decimal_places=2)
    # demo6: List[str] = Field(min_length=3, max_length=10)
    # demo7: Set[str] = Field(min_length=3, max_length=10)
    # demo8: Tuple[str] = Field(min_length=3, max_length=10)
    # email: EmailStr
    # website: HttpUrl
    # website_portfolio: AnyHttpUrl
    # server_ip: IPvAnyAddress
    # resume_path: FilePath
    # directory_path: DirectoryPath
    
    @field_validator("user_id")
    def user_id_validator(cls, value):
        if value < 100:
            raise ValueError("User id is less than 100")
        return value
    
    @field_validator("category_id")
    def category_id_validator(cls, value):
        if value < 100:
            raise ValueError("Category id is less than 100")
        
    @field_validator("name")
    def name_validator(cls, value):
        if len(value) < 3:
            raise ValueError("Product name is less than 3")
    