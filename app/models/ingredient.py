from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
  from .user import Foodie

class Ingredient(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ingredient: Mapped[str]
    foodies: Mapped[Optional[list["Foodie"]]] = relationship(
        secondary="user_ingredient", back_populates="ingredients")

    def to_dict(self):
        return {
            'id': self.id,
            'ingredient': self.ingredient,
            'foodies': [foodie.to_dict() for foodie in self.foodies]
        }
    
    @classmethod
    def from_dict(cls, data):
        return Ingredient(ingredient=data['ingredient'])
