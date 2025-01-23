from sqlalchemy.orm import Mapped
from ..db import db

class user(db.Model):
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
