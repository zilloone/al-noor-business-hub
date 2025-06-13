# app/routers/orders.py
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models import CartItem, Product, Order, OrderItem, CartItemPublic, CartItemCreate, OrderPublic
from app.api.deps import SessionDep, CurrentUser


router = APIRouter(tags=["orders"])

@router.post("/cart", response_model=CartItemPublic)
def add_to_cart(cart_item: CartItemCreate, current_user: CurrentUser, session: SessionDep):
    product = session.get(Product, cart_item.product_id)
    if not product or cart_item.quantity < 1:
        raise HTTPException(status_code=400, detail="Invalid product or quantity")

    db_cart = CartItem(
        user_id=current_user.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
    )
    session.add(db_cart)
    session.commit()
    session.refresh(db_cart)
    return db_cart


@router.get("/cart", response_model=list[CartItemPublic])
def get_cart(current_user: CurrentUser, session: SessionDep):
    
    cart_items = session.exec(select(CartItem).where(CartItem.user_id == current_user.id)).all()
    return cart_items


@router.delete("/cart/{item_id}")
def delete_cart_item(item_id: int, session: SessionDep, current_user: CurrentUser):
    item = session.get(CartItem, item_id)
    if not item or item.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found or unauthorized")
    session.delete(item)
    session.commit()
    return {"detail": "Item removed from cart"}


@router.post("/checkout", response_model=OrderPublic)
def checkout(current_user: CurrentUser, session: SessionDep):
    cart_items = session.exec(select(CartItem).where(CartItem.user_id == current_user.id)).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items = []

    for item in cart_items:
        product = session.get(Product, item.product_id)
        if not product or product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Product '{product.name}' is out of stock")
        total += product.price * item.quantity
        product.stock -= item.quantity
        session.add(product)

    order = Order(user_id=current_user.id, total_price=total)
    session.add(order)
    session.commit()
    session.refresh(order)

    for item in cart_items:
        product = session.get(Product, item.product_id)
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        session.add(order_item)

    # Clear cart
    for item in cart_items:
        session.delete(item)

    session.commit()
    return order


@router.get("/", response_model=list[OrderPublic])
def get_my_orders(current_user: CurrentUser, session: SessionDep):
    orders = session.exec(select(Order).where(Order.user_id == current_user.id)).all()
    return orders
