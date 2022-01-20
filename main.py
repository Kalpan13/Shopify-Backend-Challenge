from flask import Flask, Blueprint, jsonify, render_template
from flask_restx import Api
from ma import ma
from db import db
from resources.inventory_item import InventoryItem, InventoryItemList, items_ns, item_ns
from marshmallow import ValidationError
from loguru import logger
import sys

logger.add(sys.stderr, format="{time} | {level} : {message}", level="INFO")
logger.add("LogFile_{time}.log", rotation="1 GB", retention="1 week")

app = Flask(__name__)

bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Shopify Back-end Development Challenge')
app.register_blueprint(bluePrint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(item_ns)
api.add_namespace(items_ns)

@app.before_first_request
def create_tables():
    db.create_all()
    logger.info("Tables created in Database.")

@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

@app.route('/')
def index():
    return render_template('index.html')

item_ns.add_resource(InventoryItem, '/<int:id>')
items_ns.add_resource(InventoryItemList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run()
    