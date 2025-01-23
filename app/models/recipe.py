from sqlalchemy.orm import Mapped
from ..db import db

class recipe(db.Model):
    name: Mapped[str]
    spoonacularid: Mapped[int]
    userid: Mapped[int]

    def to_dict(self):
        return dict(
            name=self.name,
            spoonacularid=self.spoonacularid,
            userid=self.userid
        )
    
    @classmethod
    def from_dict(cls, recipe_data):
        return cls(
            name=recipe_data["name"],
            spoonacularid=recipe_data["spoonacularid"],
            userid=recipe_data["userid"]
        )
