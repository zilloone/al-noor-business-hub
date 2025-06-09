# app/models.py
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime, timezone


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    is_retailer: bool = Field(default=False)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    

class UserCreate(UserBase):
    password: str
    

class UserPublic(UserBase):
    id: int


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    username: str
    is_retailer: bool = False
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)



#Products

class ProductBase(SQLModel):
    name: str
    description: str = None
    price: float
    stock: int
    image_url: str | None = None


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
   
    retailer_id: int = Field(foreign_key="user.id")


class ProductCreate(ProductBase):
    pass
    

class ProductPublic(ProductBase):
    id: int
    retailer_id: int


class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    image_url: str | None = None


class CartItemBase(SQLModel):
    quantity: int

    
class CartItemCreate(CartItemBase):
    product_id: int


class CartItemUpdate(SQLModel):
    quantity: int | None = None


class CartItem(CartItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    product_id: int | None = Field(foreign_key="product.id")
    

class CartItemPublic(CartItemBase):
    user_id: int
    product_id: int


class OrderBase(SQLModel):
    total_price: float
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


class Order(OrderBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    

class OrderPublic(OrderBase):
    id: int


class OrderItemBase(SQLModel):
    quantity: int
    unit_price: float
    product_id: int



class OrderItem(OrderItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    
    
class OrderItemPublic(OrderItemBase):
   pass




class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


