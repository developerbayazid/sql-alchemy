from pydantic import BaseModel

    
class ProductCreate(BaseModel):
    user_id: int
    category_id: int
    name: str
    price: float
    unit: str
    img_url: str