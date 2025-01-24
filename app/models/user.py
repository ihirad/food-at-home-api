from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
  from .ingredient import Ingredient
from sqlalchemy import ForeignKey
from .recipe import Recipe


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    books: Mapped[list["Ingredient"]] = relationship(secondary="user_ingredient", back_populates="users")
    recipe_id: Mapped[Optional[int]] = mapped_column(ForeignKey("recipe.id"))
    recipe: Mapped[Optional["Recipe"]] = relationship(back_populates="users")

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email
        )
    @classmethod
    def from_dict(cls, user_data):
        return cls(
            username=user_data["username"],
            password=user_data["password"],
            email=user_data["email"])
