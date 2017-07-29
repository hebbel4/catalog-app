#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Item, User
import os
from items.items import items
from users.users import users
from jsons.jsons import jsons


app = Flask(__name__)

app.register_blueprint(items)
app.register_blueprint(users)
app.register_blueprint(jsons)




# deal with browser cache problem regarding to css file
# @app.url_defaults
# def hashed_url_for_static_file(endpoint, values):
#     if 'static' == endpoint or endpoint.endswith('.static'):
#         filename = values.get('filename')
#         if filename:
#             if '.' in endpoint:  # has higher priority
#                 blueprint = endpoint.rsplit('.', 1)[0]
#             else:
#                 blueprint = request.blueprint  # can be None too

#             if blueprint:
#                 static_folder = app.blueprints[blueprint].static_folder
#             else:
#                 static_folder = app.static_folder

#             param_name = 'h'
#             while param_name in values:
#                 param_name = '_' + param_name
#             values[param_name] = static_file_hash(
#                 os.path.join(static_folder, filename))


# def static_file_hash(filename):
#     return int(os.stat(filename).st_mtime)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
