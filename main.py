from fastapi import FastAPI, HTTPException
from database import db_session
from model import ProductModel
from schema import ProductCreate

app = FastAPI()


@app.post('/product-create')
async def create_product(data: ProductCreate):
    try:
        async with db_session() as session:
            product = ProductModel(**data.model_dump())
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return{
                "message" : "Product has been created successfully",
                "id" : product.id
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

