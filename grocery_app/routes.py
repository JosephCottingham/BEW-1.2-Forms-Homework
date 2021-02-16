from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    groceryStoreForm = GroceryStoreForm()

    if groceryStoreForm.validate_on_submit():
        # Create new ORM GroceryStore
        newGroceryStore = GroceryStore(
            title=groceryStoreForm.title.data,
            address=groceryStoreForm.address.data,
        )
        db.session.add(newGroceryStore)
        db.session.commit()
        flash('Success')
        # Send to created GroceryStore page 
        return redirect(url_for('main.store_detail', store_id=newGroceryStore.id))
    # Returned on 'GET'
    return render_template('new_store.html', groceryStoreForm=groceryStoreForm)

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    groceryItemForm = GroceryItemForm()

    if groceryItemForm.validate_on_submit():
        # Create new ORM GroceryItem
        newGroceryItem = GroceryItem(
            name=groceryItemForm.name.data,
            price=groceryItemForm.price.data,
            category=groceryItemForm.category.data,
            photo_url=groceryItemForm.photo_url.data,
            store=groceryItemForm.store.data
        )
        db.session.add(newGroceryItem)
        db.session.commit()
        flash('Success')
        # Send to created GroceryItem page 
        return redirect(url_for('main.item_detail', item_id=newGroceryItem.id))
    # Returned on 'GET'
    return render_template('new_item.html', groceryItemForm=groceryItemForm)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    groceryStoreForm = GroceryStoreForm(obj=store)
    
    if groceryStoreForm.validate_on_submit():
        # Update ORM GroceryStore
        store.title = groceryStoreForm.title.data
        store.address = groceryStoreForm.address.data
        db.session.commit()
        flash('Success')
        # Send to updated GroceryItem page (same resource) 
        return redirect(url_for('main.store_detail', store_id=store_id))

    store = GroceryStore.query.get(store_id)
    # Returned on 'GET'
    return render_template('store_detail.html', store=store, groceryStoreForm=groceryStoreForm)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    groceryItemForm = GroceryItemForm(obj=item)
    if groceryItemForm.validate_on_submit():
        # Update ORM GroceryItem
        item.name = groceryItemForm.name.data
        item.price = groceryItemForm.price.data
        item.category = groceryItemForm.category.data
        item.photo_url = groceryItemForm.photo_url.data
        item.store = groceryItemForm.store.data
        db.session.commit()
        flash('Success')
        # Send to updated GroceryItem page (same resource) 
        return redirect(url_for('main.item_detail', item_id=item_id))

    item = GroceryItem.query.get(item_id)
    # Returned on 'GET'
    return render_template('item_detail.html', item=item, groceryItemForm=groceryItemForm)

