from sqlalchemy_utils import URLType

from flask_login import UserMixin
from grocery_app import db
from grocery_app.utils import FormEnum

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

class GroceryStore(db.Model):
    """Grocery Store model."""
    __tablename__='grocery_store'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class GroceryItem(db.Model):
    """Grocery Item model."""
    __tablename__='grocery_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(URLType)
    store_id = db.Column(
        db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    shopping_lists = db.relationship('User', secondary='user_groceryitem_association')

class User(db.Model, UserMixin):
    """User model."""
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    shopping_list_items = db.relationship('GroceryItem', secondary='user_groceryitem_association')
    
class User_GroceryItem_Association(db.Model):
    """User_GroceryItem_Association Model"""
    __tablename__='user_groceryitem_association'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    groceryitem_id = db.Column(db.Integer, db.ForeignKey('grocery_item.id'), primary_key=True)
