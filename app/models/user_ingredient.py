from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class UserIngredient(db.Model):
    __tablename__ = "user_ingredient"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredient.id"), primary_key=True)
    
#     def to_dict(self):
#         return {
#             'user_id': self.user_id,
#             'ingredient_id': self.ingredient_id,
#             'quantity': self.quantity,
#             'unit': self.unit,
#         }
#     @classmethod
#     def from_dict(cls, data):
#         return UserIngredient(quantity=data['quantity'], unit=data['unit'])

# # Example JSON representation of UserIngredient
# example_json = {
#     "user_id": 1,
#     "ingredient_id": 101,
#     "quantity": 2.5,
#     "unit": "kg",
# }