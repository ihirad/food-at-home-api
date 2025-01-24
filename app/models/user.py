from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .recipe import Recipe
from sqlalchemy import ForeignKey


class Foodie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    # email: Mapped[str]
    ingredients: Mapped[Optional[list["Ingredient"]]] = relationship(secondary="user_ingredient", back_populates="foodies")
    # recipe_id: Mapped[Optional[int]] = mapped_column(ForeignKey("recipe.id"))
    recipe: Mapped[Optional[list["Recipe"]]] = relationship(back_populates="foodie")

    def to_dict(self):
        return dict(
            name=self.name,
            recipe_id=self.recipe_id
            # id=self.id,
            # username=self.username,
            # password=self.password,
            # email=self.email
        )
    @classmethod
    def from_dict(cls, user_data):
        return cls(
            username=user_data["username"],
            password=user_data["password"]
            # name=recipe_data["name"],
            # recipe=recipe_data["recipe_id"],
            # user_data=recipe_data["user_id"]
            )
            # email=user_data["email"])
