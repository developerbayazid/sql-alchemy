from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, delete, update, text, func, and_, or_, not_, Numeric, Enum as SQLEnum, Integer, BigInteger, String, Date, DateTime, select, Boolean, Float, Text, ForeignKey
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional

app = FastAPI()

# Database connection
engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/sales_db")
db_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



@app.get('/db-check')
async def db_check():
    
    try:
        conn = await engine.connect()
        await conn.close()
        return {
            "status" : "success",
            "message" : "DB Connected"
        }
    except Exception as e:
        return {
            "status" : "error",
            "message" : str(e)
        }
        

class UserValidator(BaseModel):
    firstname:str
    lastname:str
    email:str
    mobile:str
    password:str
    otp:str


class UserRole(Enum):
    admin = "admin"
    user = "user"
    manager = "manager"
     
        
DBModel = declarative_base()

class User(DBModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, index=True, unique=True)
    mobile = Column(String(20), nullable=False, index=True)
    password = Column(String(500), nullable=False)
    otp = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    
    def full_name(self):
        return f"{self.firstname} {self.lastname}"



class CategoryModel(DBModel):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    
    # Relationship
    products = relationship("ProductModel", back_populates="categories")

    

class ProductModel(DBModel):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(BigInteger, ForeignKey("categories.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
    img_url = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)
    
    # Relationship
    categories = relationship("CategoryModel", back_populates="products")
    
    
               


# class ItemDB(DBModel):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     firstname = Column(String(100), nullable=False, default='Bayazid')
#     email = Column(String(50), nullable=False, unique=True, index=True)
#     mobile = Column(String(15), nullable=True, index=True)
#     is_active = Column(Boolean, default=True)
#     password = Column(String(500), nullable=False)
#     otp = Column(String(15), nullable=True)
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#     balance = Column(Float, default=0.00)
#     bio = Column(Text, nullable=True)
#     user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
#     user_role = Column(SQLEnum(UserRole), default=UserRole.user)
#     money = Column(Numeric(10, 2), default=0.00)
    



@app.get('/get-user')
async def get_user():
    async with db_session() as session:
        results = await session.get(User, 100)
        return{
            "fullName": results.full_name(),
            "email": results.email
        }

        
@app.get('/user-list')
async def user_list():
    async with db_session() as session:
        results = await session.execute(select(User))
        data = results.scalars().all()
        return data
    
    
    
@app.post('/create-user')
async def user_create(data: UserValidator):
    try:
        async with db_session() as session:
            user = User(**data.model_dump())
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return{
                "status": "success",
                "user_id": user.id
            }
        
    except Exception as e:
        return {
            "error": str(e)
        }


@app.post('/user-create')
async def create_user(user: UserValidator):
    try:
        async with db_session() as session:
            result = User(**user.model_dump())
            session.add(result)
            await session.commit()
            return {
                "message" : "User Created successfully!"
            }
            
    except Exception as e:
        return {
            "message" : str(e)
        }




@app.post('/create-bulk-users')
async def create_bulk_users(data: List[UserValidator]):
    try:
        async with db_session() as session:
            users = [User(**eachUser.model_dump()) for eachUser in data]
            session.add_all(users)
            await session.commit()
            for eachUser in users:
                await session.refresh(eachUser)
                
            return {
                "status" : "success",
                "data" : users
            }
            
    except Exception as e:
        return {"error": str(e)}






@app.get('/product/{id}')
async def get_product(id: int):
    try:
        async with db_session() as session:
            query = select(ProductModel).where(ProductModel.id == id)
            results = await session.execute(query)
            data = results.scalars().first()
            return {
                "message" : "success",
                "data" : data
            }
    
    except Exception as e:
        return {"error": str(e)}



@app.get("/products")
async def get_all_products():
    try:
        async with db_session() as session:
            query = select(ProductModel)
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message" : "success",
                "data" : data
            }
    
    except Exception as e:
        return {
            "message" : "fail",
            "error" : str(e)
        }




@app.get('/product/price/{price}')
async def get_product_by_price(price: int):
    try:
        async with db_session() as session:
            # query = select(ProductModel).where(ProductModel.price == price)
            # query = select(ProductModel).where(ProductModel.price > price)
            query = select(ProductModel).where(ProductModel.price < price)
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}
    
    
    
    
@app.get('/product/search/{keyword}')
async def get_product_by_search(keyword: str):
    try:
        async with db_session() as session:
            query = select(ProductModel).where(ProductModel.name.ilike(f"%{keyword}%"))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}
    
    
    


@app.get('/product_in_not_in')
async def get_product_by_in_not_in():
    try:
        async with db_session() as session:
            # query = select(ProductModel).where(ProductModel.id.in_([1, 2, 3, 4]))
            query = select(ProductModel).where(ProductModel.id.not_in([1, 2, 3, 4]))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}
    
    
    
@app.get('/product_in_range')
async def get_product_by_range():
    try:
        async with db_session() as session:
            query = select(ProductModel).where(ProductModel.price.between(1000, 5000))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}




@app.get('/product_and_or_not')
async def get_product_and_or_not():
    try:
        async with db_session() as session:
            query = select(ProductModel).where(
                # and_(
                #     ProductModel.user_id == 5,
                #     ProductModel.category_id == 5
                # )
                # or_(
                #     ProductModel.user_id == 5,
                #     ProductModel.category_id == 5
                # )
                not_(
                    and_(
                        ProductModel.user_id == 5,
                        ProductModel.category_id == 5
                    )
                )
            )
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}




@app.get('/product_null')
async def get_product_by_null():
    try:
        async with db_session() as session:
            # query = select(ProductModel).where(ProductModel.price.is_(None))
            query = select(ProductModel).where(ProductModel.price.is_not(None))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}



@app.get('/string-operation/{keyword}')
async def string_operation(keyword: str):
    try:
        async with db_session() as session:
            # query = select(ProductModel).where(ProductModel.name.startswith(f"{keyword}"))
            # query = select(ProductModel).where(ProductModel.name.endswith(f"{keyword}"))
            query = select(ProductModel).where(ProductModel.name.contains(f"{keyword}"))
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message": "success",
                "data": data
            }
    except Exception as e:
        return {
            "error" : str(e)
        }




@app.get('/date-filter/{date}')
async def date_filter(date: str):
    try:
        async with db_session() as session:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            query = select(ProductModel).where(ProductModel.created_at > date_obj)
            results = await session.execute(query)
            data = results.scalars().all()
            return{
                "message": "success",
                "data" : data
            }
    except Exception as e:
        return{
            "message" : "fail",
            "error" : str(e)
        }
        
        
        
@app.get('/product-state')
async def product_states():
    try:
        async with db_session() as session:
            query = select(
                func.count(ProductModel.id),
                func.avg(ProductModel.price),
                func.max(ProductModel.price),
                func.min(ProductModel.price),
                func.sum(ProductModel.price),
            )
            results = await session.execute(query)
            data = results.one()
            return{
                "message": "success",
                "count" : data[0],
                "avg" : data[1],
                "max" : data[2],
                "min" : data[3],
                "sum" : data[4],
            }
    except Exception as e:
        return{
            "message" : "fail",
            "error" : str(e)
        }



@app.get('/raw-products')
async def raw_products():
    try:
        async with db_session() as session:
            query = text("SELECT * FROM products ORDER BY id DESC")
            results = await session.execute(query)
            data = results.mappings().all()
            return{
                "message": "success",
                "data": data
            }
    except Exception as e:
        return {"error" : str(e)}

        
        
        
@app.get('/products-offset-limit')
async def get_products_by_offset_limit():
    try:
        async with db_session() as session:
            results = await session.execute(select(ProductModel).offset(10).limit(10))
            data = results.scalars().all()
            return{
                "message":"success",
                "data": data
            }
    
    except Exception as e:
        return {"error": str(e)}
 
 
    
class ProductUpdate(BaseModel):
    id: int | None = None
    category_id: int | None = None
    name: str | None = None
    price: float | None = None
    unit: str | None = None
    img_url: str | None = None
    
# class CategoryModel(DBModel):
#     __tablename__ = "categories"
#     id = Column(Integer, primary_key=True)
        
        
        
@app.patch("/product/edit/{id}")
async def product_edit(id: int, product_data: ProductUpdate):
    try:
        async with db_session() as session:
            update_data = product_data.model_dump(exclude_unset=True)
    
            await session.execute(
                update(ProductModel)
                .where(ProductModel.id == id)
                .values(**update_data)
            )
            await session.commit()
            
            return{
                "message" : "Product updated successfully",
            }
    except Exception as e:
        return{"error": str(e)}
    
    
    
@app.patch("/all-products/edit")
async def product_edit(product_data: List[ProductUpdate]):
    try:
        async with db_session() as session:
            
            update_data = [
                product.model_dump(exclude_unset=True) for product in product_data
            ]
    
            await session.execute(
                update(ProductModel),
                update_data
            )
            await session.commit()
            
            return{
                "message" : "Product updated successfully",
            }
    except Exception as e:
        return{"error": str(e)}
        
        
@app.delete('/product/delete/{id}')
async def product_delete(id: int):
    try:
        async with db_session() as session:
    
            await session.execute(
                delete(ProductModel)
                .where(ProductModel.id == id)
            )
            await session.commit()
            
            return{
                "message" : "Product deleted successfully",
            }
    except Exception as e:
        return{"error": str(e)}
    
    
class ProductBulk(BaseModel):
    ids: List[int]
    
    
    
@app.delete('/product/delete')
async def product_delete(data: ProductBulk):
    try:
        async with db_session() as session:
    
            await session.execute(
                delete(ProductModel)
                .where(ProductModel.id.in_(data.ids))
            )
            await session.commit()
            
            return{
                "message" : "Product deleted successfully",
            }
    except Exception as e:
        return{"error": str(e)}
    
    
    
    
@app.get('/inner-join')
async def product_category_inner_join():
    try:
        async with db_session() as session:
            results = await session.execute(
                select(ProductModel, CategoryModel)
                .join(ProductModel.categories)
            )
            rows = results.all()
            return[
                {
                    "product_name" : p.name,
                    "category_name" : c.name
                }
                for p, c in rows
            ]
            
    except Exception as e:
        return {"message":"fail", "error":str(e)}
    
    

@app.get('/inner-join-reverse')
async def product_category_inner_join_reverse():
    try:
        async with db_session() as session:
            results = await session.execute(
                select(CategoryModel, ProductModel)
                .join(CategoryModel.products)
            )
            rows = results.all()
            return[
                {
                    "category_name" : c.name,
                    "product_name" : p.name
                }
                for c, p in rows
            ]
            
    except Exception as e:
        return {"message":"fail", "error":str(e)}
    
    
    
@app.get('/outer-join')
async def product_category_outer_join():
    try:
        async with db_session() as session:
            results = await session.execute(
                select(ProductModel, CategoryModel)
                .outerjoin(ProductModel.categories)
            )
            rows = results.all()
            return[
                {
                    "product": {
                        "name" : p.name,
                        "price" : p.price,
                        "unit" : p.unit
                    },
                    "category": {
                        "name" : c.name
                    } if c else None
                }
                for p, c in rows
            ]
            
    except Exception as e:
        return {"message":"fail", "error":str(e)}
    
    
    
@app.get('/outer-join-reverse')
async def product_category_outer_join_reverse():
    try:
        async with db_session() as session:
            results = await session.execute(
                select(CategoryModel, ProductModel)
                .outerjoin(CategoryModel.products)
            )
            rows = results.all()
            return[
                {
                    "category": {
                        "name": c.name
                    },
                    "product": {
                        "name": p.name,
                        "price": p.price,
                        "unit" : p.unit
                    } if p else None
                }
                for c, p in rows
            ]
            
    except Exception as e:
        return {"message":"fail", "error":str(e)}