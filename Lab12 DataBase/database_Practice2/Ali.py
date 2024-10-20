
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'  # SQLite database file
db = SQLAlchemy(app)



# Define Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    brand = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='product', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

# Create the database tables
def create_database():
    db.create_all()
    load_data_from_csv()
    db.session.commit()

# Load data from CSV files into the database
def load_data_from_csv():
    products_data = pd.read_csv('PRO.csv')
    reviews_data = pd.read_csv('Reviews.csv')

    for _, product_row in products_data.iterrows():
        product = Product(
            name=product_row['Name'],
            price=product_row['Price'],
            brand=product_row['Brand']
        )
        db.session.add(product)
        db.session.commit()

    for _, review_row in reviews_data.iterrows():
        review = Review(
            review_text=review_row['Reviews'],
            product_id=review_row['Id']
        )
        db.session.add(review)
        db.session.commit()

# Uncomment the following line if you want to load data when the application starts
# load_data_from_csv()

# Routes
@app.route('/')
def index():
    all_products = Product.query.all()
    return render_template('index1.html', products=all_products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    return render_template('product_details.html', product=product)

if __name__ == '__main__':
    with app.app_context():
        create_database()
    app.run(debug=True)