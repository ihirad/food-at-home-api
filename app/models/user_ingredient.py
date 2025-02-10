from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime, date
from ..db import db

class UserIngredient(db.Model):
    __tablename__ = "user_ingredient"
    foodie_id: Mapped[int] = mapped_column(ForeignKey("foodie.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredient.id"), primary_key=True)
    expiration_date: Mapped[Optional[date]] = mapped_column(default=None)


    def to_dict(self):
        return {
            'foodie_id': self.foodie_id,
            'ingredient_id': self.ingredient_id,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return UserIngredient(
            foodie_id=data['foodie_id'],
            ingredient_id=data['ingredient_id'],
            expiration_date=data['expiration_date']
        )
