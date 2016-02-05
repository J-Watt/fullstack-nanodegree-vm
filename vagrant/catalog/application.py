from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session as login_session
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2, json, requests, random, string
from datetime import datetime

from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def index():
    categories = session.query(Category)
    items = session.query(Item).order_by(Item.id.desc()).limit(10)
    dbinfo = {"categories": categories, "items": items, "current": ""}
    return render_template('index.html', dbinfo=dbinfo,)

@app.route('/catalog/<category_name>/')
def category(category_name):
    categories = session.query(Category)
    items = session.query(Item).filter(Item.category.has(name = category_name))
    dbinfo = {"categories": categories, "items": items, "current": category_name}
    return render_template('category.html', dbinfo=dbinfo)

@app.route('/catalog/<category_name>/<item_name>/', defaults = {'item_id': None})
@app.route('/catalog/<category_name>/<item_name>.<int:item_id>/')
def item(category_name, item_name, item_id):
    if item_id:
        current = session.query(Item).filter(Item.id == item_id, Item.name == item_name, Item.category.has(name = category_name)).one()
    else:
        current = session.query(Item).filter(Item.name == item_name, Item.category.has(name = category_name)).order_by(id.desc()).first()
    categories = session.query(Category)
    items = session.query(Item).filter(Item.category.has(name = category_name))
    creator = getUserInfo(current.user_id)
    dbinfo = {"categories": categories, "items": items, "current": current}
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicitem.html', dbinfo=dbinfo)
    else:
        return render_template('item.html', dbinfo=dbinfo)

@app.route('/catalog/new/', methods = ['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newitem = Item(name = request.form['name'], description = request.form['description'], image = request.form['image'], category_id = request.form['category'], user_id = login_session['user_id'])
        session.add(newitem)
        session.commit()
        current = session.query(Item).filter(Item.name == request.form['name'], Item.user_id == login_session['user_id']).first()
        flash("new item has been created!")
        return redirect(url_for('category', category_name = current.category.name))
    else:
        categories = session.query(Category)
        dbinfo = {"categories": categories, "current": ""}
        return render_template('newitem.html', dbinfo=dbinfo)

@app.route('/catalog/<category_name>/<item_name>.<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(category_name, item_name, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    edititem = session.query(Item).filter_by(id = item_id).one()
    if edititem.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()' >")
    if request.method == 'POST':
        if request.form['name']:
            edititem.name = request.form['name']
        if request.form['description']:
            edititem.description = request.form['description']
        if request.form['image']:
            edititem.image = request.form['image']
        if request.form['category_id']:
            edititem.category_id = request.form['category_id']
        session.add(edititem)
        session.commit()
        flash("item has been edited!")
        items = session.query(Item).filter_by(id = item_id).one()
        return redirect(url_for('item', category_name = items.category.name, item_name = items.name, item_id = items.id))
    else:
        categories = session.query(Category)
        items = session.query(Item).filter_by(category_id = edititem.category_id)
        dbinfo = {"categories": categories, "items": items, "current": edititem}
        return render_template('edititem.html', dbinfo=dbinfo)

@app.route('/catalog/<category_name>/<item_name>.<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(category_name, item_name, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleteitem = session.query(Item).filter_by(id = item_id).one()
    if deleteitem.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not authorized to delete this item. Please create your own item in order to delete.');}</script><body onload='myFunction()' >")
    current = deleteitem.category.name
    if request.method == 'POST':
        session.delete(deleteitem)
        session.commit()
        flash("item has been deleted!")
        return redirect(url_for('category', category_name = current))
    else:
        categories = session.query(Category)
        items = session.query(Item).filter_by(category_id = deleteitem.category_id)
        dbinfo = {"categories": categories, "items": items, "current": deleteitem}
        return render_template('deleteitem.html', dbinfo=dbinfo)

@app.route('/catalog/user/<int:user_id>/')
def userItems(user_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category)
    items = session.query(Item).filter_by(user_id = user_id)
    dbinfo = {"categories": categories, "items": items, "current": ""}
    return render_template('useritems.html', dbinfo=dbinfo)

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        #Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    #If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    #Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID doesn't match application."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    #Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    #Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = (data['email']).lower()

    #See if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = "<h1>Welcome, " + login_session['username'] + "!</h1><img src='" + login_session['picture'] + "' style = 'width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;'> "
    flash ("you are now logged in as %s" % login_session['username'])
    return output

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    #Exchange client token for long-lived server side token with GET /oauth/
    #access token?grant_type=fb_exchange_token&client_id={app-
    #id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    #Use token to get user info from API
    userinfo_url = "https//graph.facebook.com/v2.5/me"
    #strip expire tag from access token
    token = result.split("&")[0]

    url = "https://graph.facebook.com/v2.5/me?%s&fields=name,id,email" % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    #print ("url sent for API access:%s" % url)
    #print ("API JSON result: %s" % result)
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = (data['email']).lower()
    login_session['facebook_id'] = data['id']

    #Token stored in login_session in order to properly logout
    login_session['access_token'] = token

    #Get user picture
    url = 'https://graph.facebook.com/v2.5/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data['data']['url']

    #See if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = "<h1>Welcome, " + login_session['username'] + "!</h1><img src='" + login_session['picture'] + "' style = 'width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;'> "
    flash ("you are now logged in as %s" % login_session['username'])
    return output

#DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    #Only disconnect a connected user
    access_token = login_session.get('credentials')
    if access_token is None:
        response = make_response(json.dumps("Current user not connected."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Execute HTTP GET request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        #For whatever reason, the given token was invalid
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == "google":
            gdisconnect()
            del login_session['credentials']
            del login_session['gplus_id']
        if login_session['provider'] == "facebook":
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('index'))
    else:
        flash("You were not logged in")
        return redirect(url_for('index'))

#API Endpoint (GET Request)
@app.route('/catalog/JSON')
def catalogJSON():
    items = session.query(Item).all()
    return jsonify(Items = [i.serialize for i in items])

#API Endpoint (GET Request) for categories
@app.route('/catalog/<int:category_id>/JSON')
def catalogCategoryJSON(category_id):
    categories = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return jsonify(Items = [i.serialize for i in items])

#API Endpoint (GET Request) for items
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def catalogItemJSON(category_id, item_id):
    items = session.query(Item).filter_by(id = item_id).one()
    return jsonify(Items = items.serialize)

#API Endpoint
@app.route('/catalog/ATOM')
def catalog_feed():
    feed = AtomFeed('Recent Items',
                    feed_url = request.url, url = request.url_root)
    items = session.query(Item).order_by(Item.id.desc()).limit(10).all()
    for i in items:
        feed.add(i.name, unicode(i.description), content_type = 'html',
                 author = i.user.name, url = make_external(url_for("item", category_name = i.category.name, item_name = i.name, item_id = i.id)),
                 updated = i.date)
    return feed.get_response()

def make_external(url):
    return urljoin(request.url_root, url)

def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

if __name__ == '__main__':
    app.secret_key = '\xf9;\x14\x13\xad\xda\xa8bk\x94\xdaa'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)