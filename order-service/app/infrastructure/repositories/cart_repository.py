from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.infrastructure.database.models import CartModel, CartItemModel


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_by_user_id(self, user_id: str) -> CartModel:
        cart = self.get_by_user_id(user_id)
        if cart:
            return cart
        cart = CartModel(user_id=user_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def get_by_user_id(self, user_id: str) -> CartModel | None:
        stmt = (
            select(CartModel)
            .where(CartModel.user_id == user_id)
            .options(selectinload(CartModel.items))
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def add_item(self, cart: CartModel, product_id: str, product_name: str, unit_price, quantity: int) -> CartModel:
        existing_item = next((item for item in cart.items if item.product_id == product_id), None)

        if existing_item:
            existing_item.quantity += quantity
            existing_item.unit_price = unit_price
            existing_item.product_name = product_name
        else:
            self.db.add(
                CartItemModel(
                    cart_id=cart.id,
                    product_id=product_id,
                    product_name=product_name,
                    unit_price=unit_price,
                    quantity=quantity,
                )
            )

        self.db.commit()
        return self.get_by_user_id(cart.user_id)

    def remove_item(self, user_id: str, product_id: str) -> CartModel | None:
        cart = self.get_by_user_id(user_id)
        if not cart:
            return None

        item = next((item for item in cart.items if item.product_id == product_id), None)
        if item:
            self.db.delete(item)
            self.db.commit()

        return self.get_by_user_id(user_id)

    def clear_cart(self, user_id: str) -> None:
        cart = self.get_by_user_id(user_id)
        if not cart:
            return

        for item in list(cart.items):
            self.db.delete(item)
        self.db.commit()
