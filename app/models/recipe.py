from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .user import Foodie

class Recipe(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    foodie_id: Mapped[int] = mapped_column(ForeignKey('foodie.id'))
    foodie: Mapped["Foodie"] = relationship(back_populates='recipes')

    def to_dict(self):
        return dict(
            name=self.name,
            recipe_id=self.recipe_id,
            # user_id=self.user_id,
            # user= self.user.to_dict() if self.user else None
            # users=[user.to_dict() for user in self.user]
        )
    
    @classmethod
    def from_dict(cls, recipe_data):
        return cls(
            name=recipe_data["name"],
            recipe_id=recipe_data["recipe_id"],
            user_id=recipe_data["user_id"]
        )
