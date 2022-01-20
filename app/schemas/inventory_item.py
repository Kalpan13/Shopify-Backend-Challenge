from ma import ma
from models.inventory_item import InventoryItemModel


class InventoryItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryItemModel
        load_instance = True
        