from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import (
    GroceryStore,
    GroceryItem,
    User,
)
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, LoginForm, SignUpForm

from flask_login import login_required, login_user, logout_user, current_user

# Import app and db from events_app package so that we can run app
from grocery_app import app, db, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################


# MAIN ROUTES


@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores, current_user=current_user)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    groceryStoreForm = GroceryStoreForm()

    if groceryStoreForm.validate_on_submit():
        # Create new ORM GroceryStore
        newGroceryStore = GroceryStore(
            title=groceryStoreForm.title.data,
            address=groceryStoreForm.address.data,
            created_by=current_user
        )
        db.session.add(newGroceryStore)
        db.session.commit()
        flash('Success')
        # Send to created GroceryStore page 
        return redirect(url_for('main.store_detail', store_id=newGroceryStore.id))
    # Returned on 'GET'
    return render_template('new_store.html', groceryStoreForm=groceryStoreForm, current_user=current_user)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    groceryItemForm = GroceryItemForm()
    if groceryItemForm.validate_on_submit():
        print('safdas')
        # Create new ORM GroceryItem
        newGroceryItem = GroceryItem(
            name=groceryItemForm.name.data,
            price=groceryItemForm.price.data,
            category=groceryItemForm.category.data,
            photo_url=groceryItemForm.photo_url.data,
            store=groceryItemForm.store.data,
            created_by=current_user
        )
        db.session.add(newGroceryItem)
        db.session.commit()
        flash('Success')
        # Send to created GroceryItem page 
        return redirect(url_for('main.item_detail', item_id=newGroceryItem.id))
    # Returned on 'GET'
    return render_template('new_item.html', groceryItemForm=groceryItemForm, current_user=current_user)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
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
    return render_template('store_detail.html', store=store, groceryStoreForm=groceryStoreForm, current_user=current_user)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
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
    return render_template('item_detail.html', item=item, groceryItemForm=groceryItemForm, current_user=current_user)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = db.session.query(GroceryItem).get(item_id)
    if item != None:
        current_user.shopping_list_items.append(item)
        db.session.commit()
    return redirect(url_for('main.shopping_list'))

@main.route('/shopping_list')
@login_required
def shopping_list():
    return render_template('shopping_cart.html', current_user=current_user)



# AUTH ROUTES


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form, current_user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form, current_user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

