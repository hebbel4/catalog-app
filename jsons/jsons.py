from flask import Flask
from flask import jsonify
from flask import Blueprint
from db_setup import Base, Category, Item, User
import random
from database import session


# Define the Blueprint
jsons = Blueprint('jsons', __name__)

# my API endpoint
@jsons.route('/catalog.json')
def json_func():
    rand = random.randrange(0, session.query(Item).count())
    ran_item = session.query(Item)[rand]
    return jsonify(ran_item.serialize)


@jsons.route('/catalog.json/all_items/')
def json_all_items():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


@jsons.route('/catalog.json/category/')
def json_category():
    rand = random.randrange(0, session.query(Category).count())
    rand_cat = session.query(Category)[rand]
    return jsonify(rand_cat.serialize)