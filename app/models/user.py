from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from ..db import db
from typing import TYPE_CHECKING, Optional
# from werkzeug.security import check_password_hash
if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .recipe import Recipe
    from .shopping_note import ShoppingNote


class Foodie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username: Mapped[str]
    # password: Mapped[str]
    email: Mapped[Optional[str]] 
    ingredients: Mapped[Optional[list["Ingredient"]]] = relationship(
        secondary="user_ingredient", back_populates="foodies")
    recipes: Mapped[Optional[list["Recipe"]]] = relationship(back_populates="foodie") 
    shopping_notes: Mapped[Optional[list["ShoppingNote"]]] = relationship(back_populates="foodie")

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            # password=self.password,
            email=self.email,
        )
    
    @classmethod
    def from_dict(cls, user_data):
        return cls(
            username=user_data["username"],
            # password=user_data["password"],
            email=user_data["email"]
            )
    # def check_password(self, password):

    #     return check_password_hash(self.password, password)


