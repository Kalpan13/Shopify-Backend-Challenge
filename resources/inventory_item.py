from flask import request
from flask_restx import Resource, fields, Namespace
from loguru import logger
from models.inventory_item import InventoryItemModel
from schemas.inventory_item import InventoryItemSchema
import sqlalchemy

ITEM_NOT_FOUND = "Item not found."

item_ns = Namespace('inventory_item', description='Item related operations')
items_ns = Namespace('inventory_items', description='Items related operations')

item = items_ns.model('InventoryItem', {
    'name': fields.String('Name of the Item'),
    'price': fields.Float(0.00),
    'quantity': fields.Integer(1)
})

item_schema = InventoryItemSchema()
item_list_schema = InventoryItemSchema(many=True)

class InventoryItem(Resource):

    def get(self, id):
        item_data = InventoryItemModel.find_by_id(id)
        if item_data:
            return item_schema.dump(item_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self,id):
        item_data = InventoryItemModel.find_by_id(id)
        if item_data:
            item_data.delete_from_db()
            return {'message': "Item Deleted successfully"}, 200
        return {'message': ITEM_NOT_FOUND}, 404

    @item_ns.expect(item)
    def put(self, id):
        item_data = InventoryItemModel.find_by_id(id)
        item_json = request.get_json()

        if item_data:
            for key in item_json.keys():
                item_data[key] = item_json[key]
        else:
            item_data = item_schema.load(item_json)

        item_data.save_to_db()
        return item_schema.dump(item_data), 200

class InventoryItemList(Resource):
    @items_ns.doc('Get all the Items')
    def get(self):
        return item_list_schema.dump(InventoryItemModel.find_all()), 200

    @item_ns.expect(item)
    @items_ns.doc('Create an Item')
    def post(self):
        item_json = request.get_json()
        item_data = item_schema.load(item_json)
        try:
            item_data.save_to_db()
        except sqlalchemy.exc.IntegrityError as e:
            logger.debug(f"Exception while saving item data : {item_data}")
            logger.exception(e)
            return {"error":"Unique constraint violatied"}, 409
        except Exception as e:
            logger.debug(f"Exception while saving item data : {item_data}")
            logger.exception(e)
            return {"error":"Something went wrong"}, 404
        return item_schema.dump(item_data), 201