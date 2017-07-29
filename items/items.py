from flask import Flask, render_template, request, redirect, url_for, flash
from functools import wraps
from db_setup import Base, Category, Item, User
from flask import Blueprint
import random
import string
import os
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from database import session

# Define the Blueprint
items = Blueprint('items', __name__)


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# a helper function to check user login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/')
    return decorated_function


# add an item
@login_required
@items.route('/catalog/add/', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        user = getUserInfo(login_session['user_id'])
        category_name = request.form['genre']
        category = session.query(Category).filter_by(name=str(category_name)).one()
        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       category=category, user_id=login_session['user_id'],
                       user=user)
        session.add(newItem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('users.display_all'))
    else:
        return render_template('add_item.html')


# edit item after login
@login_required
@items.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
def edit_item(item_name):
    item = session.query(Item).filter_by(title=item_name).one()
    if item.user_id == login_session['user_id']:
        if request.method == 'POST':
            if request.form['title']:
                item.title = request.form['title']
            if request.form['description']:
                item.description = request.form['description']
            category_name = request.form['genre']
            category = session.query(Category).filter_by(name=str(category_name)
                                                         ).one()
            item.category = category
            session.add(item)
            session.commit()
            flash("Item has been edited.")
            return redirect(url_for('users.display_all'))
        else:
            return render_template('edit_item.html', item_name=item.title)
    else:
        redirect(url_for('users.display_all'))


# delete item after login
@login_required
@items.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
def delete_item(item_name):
    item = session.query(Item).filter_by(title=item_name).one()
    if item.user_id == login_session['user_id']:
        if request.method == 'POST':
            session.delete(item)
            session.commit()
            flash("Item has been deleted.")
            return redirect(url_for('users.display_all'))
        else:
            return render_template('delete_item.html', item_name=item.title)
    else:
        redirect(url_for('users.display_all'))

