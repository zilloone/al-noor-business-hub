# app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from app.models import Product, ProductCreate, ProductPublic, User, ProductUpdate
from app.api.deps import CurrentUser, SessionDep
from app.core.db import engine

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/add-product", response_model=ProductPublic)
def create_product(
    product_create: ProductCreate,
    current_user: CurrentUser,
    session: SessionDep
):
    if not current_user.is_retailer:
        raise HTTPException(status_code=403, detail="Only retailers can add products")
    db_product = Product(**product_create.model_dump(), retailer_id=current_user.id)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
        

@router.get("/all", response_model=list[ProductPublic])
def list_products(session: SessionDep):
    return session.exec(select(Product)).all()


@router.get("/me", response_model=list[ProductPublic])
def list_my_products(current_user: CurrentUser, session: SessionDep):
    if not current_user.is_retailer:
        raise HTTPException(status_code=403, detail="Only retailers can view their products")
    return session.exec(select(Product).where(Product.retailer_id == current_user.id)).all()
    

@router.patch("/{product_id}", response_model=ProductPublic)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    current_user: CurrentUser,
    session: SessionDep
):
    
    product = session.get(Product, product_id)
    if not product or product.retailer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found or not yours")
    product_data = product_in.model_dump(exclude_unset=True)
    product.sqlmodel_update(product_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: SessionDep, 
    current_user: CurrentUser
):

    product = session.get(Product, product_id)
    if not product or product.retailer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found or not yours")
    session.delete(product)
    session.commit()
    return {"detail": "Product deleted"}
