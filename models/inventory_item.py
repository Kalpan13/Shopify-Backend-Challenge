from db import db
from typing import List

class InventoryItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False, )
    quantity = db.Column(db.Integer)

    def __init__(self, name, price, quantity=1, description=""):

        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description  
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name) -> "InventoryItemModel":
        return cls.query.filter_by(name = name).first()

    @classmethod
    def find_by_id(cls, id) -> "InventoryItemModel":
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_all(cls) -> List["InventoryItemModel"]:
        return cls.query.all()

        