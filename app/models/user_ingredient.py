from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class UserIngredient(db.Model):
    __tablename__ = "user_ingredient"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredient.id"), primary_key=True)
    quantity: Mapped[float]
    unit: Mapped[str]

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'ingredient_id': self.ingredient_id,
            'quantity': self.quantity,
            'unit': self.unit,
        }
    @classmethod
    def from_dict(cls, data):
        return UserIngredient(quantity=data['quantity'], unit=data['unit'])
    