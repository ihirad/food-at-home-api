from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import Foodie


class ShoppingNote(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    note: Mapped[str]
    foodie_id: Mapped[int] = mapped_column(ForeignKey('foodie.id'))
    foodie: Mapped["Foodie"] = relationship(back_populates='shopping_notes')

    def to_dict(self):
        return {
            'id': self.id,
            'note': self.note,
            'foodie': self.foodie.to_dict() if self.foodie else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return ShoppingNote(note=data['note'],
            foodie_id=data['foodie_id'])
    