from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .recipe import Recipe


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    # email: Mapped[str]
    ingredients: Mapped[list["Ingredient"]] = relationship(secondary="user_ingredient", back_populates="users")
    recipes: Mapped[list["Recipe"]] = relationship(back_populates="user") 

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email,
            # ingredients=[ingredient.to_dict() for ingredient in self.ingredients],
        )
    
    @classmethod
    def from_dict(cls, user_data):
        return cls(
            username=user_data["username"],
            password=user_data["password"],
            email=user_data["email"])
    
# Example JSON representation of User 
example_json = {
    "id": 1,
    "username": "john_doe",
    "email": "johndoe@example.com",
    "ingredients": [
        {
            "id": 1,
            "name": "Sugar",
        },
        {
            "id": 2,
            "name": "Flour",
        },
        {
            "id": 3,
            "name": "Eggs",
        }
    ]
}

