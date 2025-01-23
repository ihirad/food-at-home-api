from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .user import User

class Ingredient(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    user: Mapped[list["User"]] = relationship(
        secondary="user_ingredient", back_populates="ingredients")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'users': [user.to_dict() for user in self.user]
        }
    
    @classmethod
    def from_dict(cls, data):
        return Ingredient(name=data['name'])
