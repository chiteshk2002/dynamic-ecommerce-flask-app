from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    features = db.Column(db.Text, nullable=True)         
    materials = db.Column(db.String(200), nullable=True)  
    care_instructions = db.Column(db.Text, nullable=True) 
    release_date = db.Column(db.String(50), nullable=True)
    image = db.Column(db.String(200), nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    card_name = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    expiry = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.String(5), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    items = db.relationship('OrderDetail', backref='order', lazy=True)

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    subtotal = db.Column(db.Float)

    product = db.relationship("Product", backref="order_items")
