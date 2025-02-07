from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from ..db import db
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
  from .user import Foodie

class Recipe(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    recipe_id: Mapped[int]
    image: Mapped[Optional[str]]
    favorite: Mapped[Optional[bool]] = mapped_column(default=False)
    foodie_id: Mapped[int] = mapped_column(ForeignKey('foodie.id'))
    foodie: Mapped["Foodie"] = relationship(back_populates='recipes')

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            recipe_id=self.recipe_id,
            image=self.image,
            favorite=self.favorite
            
        )
    
    @classmethod
    def from_dict(cls, recipe_data):
        return cls(
            name=recipe_data["name"],
            recipe_id=recipe_data["recipe_id"],
            image=recipe_data["image"],
            favorite=recipe_data["favorite"],
            foodie_id=recipe_data["foodie_id"]
        )
