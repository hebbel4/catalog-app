from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Item
import os
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(\
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "My Catalog app"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
'''
# displays the initial website
@app.route('/')
def display_all():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).all()   
    return render_template('display_all.html', categories = categories, \
                           items = items, STATE = state)

# show items for each category
@app.route('/catalog/<string:category_name>/items/')
def show_items(category_name):
    categories = session.query(Category).all()
    curr_category = session.query(Category).filter_by(name = category_name)\
                    .one()
    items = session.query(Item).filter_by(category = curr_category)
    return render_template('show_items.html', categories = categories, \
                           items = items, category_name = category_name)
    
# show description of item
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def show_info(category_name, item_name):
    item = session.query(Item).filter_by(title = item_name).one()
    return render_template('show_info.html', item = item)
'''

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token'] 
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:
	
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response

# display after login
@app.route('/')
def display_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).all()   
    return render_template('display_login.html', categories = categories, \
                           items = items, STATE = state)

# add an item
@app.route('/catalog/add/', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        category_name = request.form['genre']
        category = session.query(Category).filter_by(name = str(category_name)\
                                                     ).one()
        newItem = Item(title = request.form['title'], description = \
                       request.form['description'], category = category)
        session.add(newItem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('display_login'))
    else:
        return render_template('add_item.html')

# show items after login
@app.route('/catalog/<string:category_name>/items/')
def show_items_login(category_name):
    categories = session.query(Category).all()
    curr_category = session.query(Category).filter_by(name = category_name)\
                    .one()
    items = session.query(Item).filter_by(category = curr_category)
    return render_template('show_items_login.html', categories = categories, \
                           items = items, category_name = category_name)

# show description of item after login
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def show_info_login(category_name, item_name):
    item = session.query(Item).filter_by(title = item_name).one()
    return render_template('show_info_login.html', item = item)

# edit item after login
@app.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
def edit_item(item_name):
    item = session.query(Item).filter_by(title = item_name).one()
    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        category_name = request.form['genre']
        category = session.query(Category).filter_by(name = str(category_name)\
                                                     ).one()
        item.category = category
        session.add(item)
        session.commit()
        flash("Item has been edited.")
        return redirect(url_for('display_login'))
    else:
        return render_template('edit_item.html', item_name = item.title)
    
# delete item after login
@app.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
def delete_item(item_name):
    item = session.query(Item).filter_by(title = item_name).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item has been deleted.")
        return redirect(url_for('display_login'))
    else:
        return render_template('delete_item.html', item_name = item.title)

# deal with browser cache problem regarding to css file
@app.url_defaults
def hashed_url_for_static_file(endpoint, values):
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            if '.' in endpoint:  # has higher priority
                blueprint = endpoint.rsplit('.', 1)[0]
            else:
                blueprint = request.blueprint  # can be None too

            if blueprint:
                static_folder = app.blueprints[blueprint].static_folder
            else:
                static_folder = app.static_folder

            param_name = 'h'
            while param_name in values:
                param_name = '_' + param_name
            values[param_name] = static_file_hash(os.path.join(static_folder, filename))
            
def static_file_hash(filename):
  return int(os.stat(filename).st_mtime)

# my API endpoint
@app.route('/catalog.json')
def json():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
