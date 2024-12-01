from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Product, db
from app.forms import LoginForm, RegisterForm
import json

app = Blueprint('app', __name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email already registered.")
            return redirect(url_for('app.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            return redirect(url_for('app.products'))
        else:
            flash("Invalid email.")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('app.index'))


@app.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@app.route('/wishlist')
@login_required
def wishlist():
    return render_template('wishlist.html')


@app.route('/wishlist/add', methods=['POST'])
@login_required
def add_to_wishlist():
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    product_description = request.form.get('product_description')
    product_price = request.form.get('product_price')

    # Retrieve the wishlist from the session
    wishlist = session.get('wishlist', [])

    # Check if the product is already in the wishlist
    if not any(product['id'] == product_id for product in wishlist):
        # Add product to wishlist
        wishlist.append({
            'id': product_id,
            'name': product_name,
            'description': product_description,
            'price': product_price
        })
        session['wishlist'] = wishlist
        flash(f'{product_name} added to wishlist!')
    else:
        flash(f'{product_name} is already in your wishlist!')

    return redirect(url_for('app.products'))


@app.route('/wishlist/remove', methods=['POST'])
@login_required
def remove_from_wishlist():
    product_id = request.form.get('product_id')

    # Retrieve the wishlist from the session
    wishlist = session.get('wishlist', [])

    # Remove the product from the wishlist
    wishlist = [product for product in wishlist if product['id'] != product_id]
    session['wishlist'] = wishlist

    flash('Product removed from wishlist!')
    return redirect(url_for('app.wishlist'))


@app.route('/like', methods=['POST'])
@login_required
def like_product():
    data = json.loads(request.data)
    product_id = int(data.get('product_id'))
    print(f"Liking product with ID: {product_id}")
    product = Product.query.get(product_id)
    if product:
        product.likes += 1
        db.session.commit()
        print(f"Product {product.name} now has {product.likes} likes")
        return jsonify({'status': 'OK', 'message': f'Product {product.name} liked!', 'likes': product.likes})
    print("Product not found")
    return jsonify({'status': 'Error', 'message': 'Product not found'}), 404
