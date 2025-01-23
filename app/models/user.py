from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]

    def to_dict(self):
        return dict(
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
