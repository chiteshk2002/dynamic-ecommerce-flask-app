from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import CheckoutForm
from models import db, Product, Order, OrderDetail

app = Flask(__name__)
app.secret_key = 'sneaksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()
    if Product.query.count() == 0:
        products = [
    Product(
        name="Nike Air Max", brand="Nike", price=220,
        description="Comfortable and iconic streetwear essential.",
        features="Max Air cushioning, lightweight mesh upper, rubber outsole.",
        materials="Mesh, Synthetic Leather, Rubber",
        care_instructions="Clean with a damp cloth. Do not machine wash.",
        release_date="2022-09-01", image="nike1.jpg"
    ),
    Product(
        name="Adidas Ultra Boost", brand="Adidas", price=180,
        description="Responsive cushioning and sleek style.",
        features="Boost midsole, Primeknit upper, Stretchweb outsole.",
        materials="Textile, Rubber",
        care_instructions="Wipe with soft brush. Avoid water immersion.",
        release_date="2023-01-10", image="adidas1.jpg"
    ),
    Product(
        name="Puma RS-X", brand="Puma", price=160,
        description="Chunky retro sneaker with futuristic style.",
        features="Mesh upper, PU midsole, TPU heel piece.",
        materials="Mesh, PU, Rubber",
        care_instructions="Air dry after light cleaning.",
        release_date="2022-11-15", image="puma1.jpg"
    ),
    Product(
        name="New Balance 550", brand="New Balance", price=190,
        description="Classic 90s basketball-inspired sneaker.",
        features="Leather upper, perforated panels, retro silhouette.",
        materials="Leather, Rubber",
        care_instructions="Use leather cleaner. Avoid prolonged moisture.",
        release_date="2023-03-01", image="newbalance1.jpg"
    ),
    Product(
        name="Converse Chuck 70", brand="Converse", price=150,
        description="Timeless canvas shoe with modern comfort.",
        features="Canvas upper, OrthoLite cushioning, rubber toe cap.",
        materials="Canvas, Rubber",
        care_instructions="Hand wash gently. Avoid bleach.",
        release_date="2021-08-10", image="converse1.jpg"
    ),
    Product(
        name="Air Jordan 1", brand="Nike", price=255,
        description="Iconic basketball silhouette with unmatched street appeal.",
        features="Air-Sole unit, leather overlays, high-top design.",
        materials="Leather, Nylon, Rubber",
        care_instructions="Use sneaker wipes. Air dry only.",
        release_date="2023-05-25", image="jordan1.jpg"
    ),
]
        db.session.bulk_save_objects(products)
        db.session.commit()


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=total)


@app.route('/remove/<int:product_id>')
def remove_item(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    updated_cart = {}

    for key, value in request.form.items():
        if key.startswith('quantities['):
            product_id = key.split('[')[1].split(']')[0]
            try:
                quantity = int(value)
                if quantity > 0:
                    updated_cart[product_id] = quantity
            except ValueError:
                continue  # Skip invalid entries

    session['cart'] = updated_cart
    return redirect(url_for('cart'))



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    cart = session.get('cart', {})
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})

    if form.validate_on_submit():
        order = Order(
            full_name=form.full_name.data,
            email=form.email.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            country=form.country.data,
            card_name=form.card_name.data,
            card_number=form.card_number.data,
            expiry=form.expiry.data,
            cvv=form.cvv.data,
            total_price=total
        )
        db.session.add(order)
        db.session.commit()

        for item in items:
            detail = OrderDetail(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['qty'],
                subtotal=item['subtotal']
            )
            db.session.add(detail)

        db.session.commit()
        session['cart'] = {}
        return redirect(url_for('confirmation', order_id=order.id))

    return render_template('checkout.html', form=form, items=items, total=total)


@app.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    order_details = OrderDetail.query.filter_by(order_id=order.id).all()
    return render_template('confirmation.html', order=order, items=order_details, total=order.total_price)


if __name__ == "__main__":
    app.run(debug=True)
