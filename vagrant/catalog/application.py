from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def index():
    categories = session.query(Category)
    return render_template('index.html', categories=categories)

@app.route('/catalog/<int:category_id>/')
def category(category_id):
    categories = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return render_template('category.html', categories=categories, items=items)

@app.route('/catalog/<int:category_id>/<int:item_id>/')
def item(category_id, item_id):
    categories = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(id = item_id).one()
    return render_template('item.html', categories=categories, items=items)

@app.route('/catalog/new/', methods = ['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        newitem = Item(name = request.form['name'], description = request.form['description'], category_id = request.form['category'])
        session.add(newitem)
        session.commit()
        flash("new item has been created!")
        return redirect(url_for('category', category_id = request.form['category']))
    else:
        categories = session.query(Category)
        return render_template('newitem.html', categories = categories)

@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
    edititem = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edititem.name = request.form['name']
        if request.form['description']:
            edititem.description = request.form['description']
        if request.form['category_id']:
            edititem.category_id = request.form['category_id']
        session.add(edititem)
        session.commit()
        flash("item has been edited!")
        items = session.query(Item).filter_by(id = item_id).one()
        return redirect(url_for('item', category_id = items.category_id, item_id = items.id))
    else:
        categories = session.query(Category)
        return render_template('edititem.html', categories=categories, items=edititem)

@app.route('/catalog/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(item_id):
    deleteitem = session.query(Item).filter_by(id = item_id).one()
    category_id = deleteitem.category_id
    if request.method == 'POST':
        session.delete(deleteitem)
        session.commit()
        flash("item has been deleted!")
        return redirect(url_for('category', category_id = category_id))
    else:
        return render_template('deleteitem.html', items=deleteitem)

#API Endpoint (GET Request) for categories
@app.route('/catalog/<int:category_id>/JSON/')
def catalogCategoryJSON(category_id):
    categories = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return jsonify(Items = [i.serialize for i in items])

#API Endpoint (GET Request) for items
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON/')
def catalogItemJSON(category_id, item_id):
    items = session.query(Item).filter_by(id = item_id).one()
    return jsonify(Items = items.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)