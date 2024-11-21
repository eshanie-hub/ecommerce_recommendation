from flask import Flask, request, render_template
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# load files
trending_products = pd.read_csv("models/trending_products.csv")
train_data = pd.read_csv("models/clean_data.csv")

# database configuration
app.secret_key = "werwerwt"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/ecom"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# model class for the signup table
class signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# model class for the signIn table
class signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text
#routes
random_image_urls = [
    "static/img/img_1.png",
    "static/img/img_2.png",
    "static/img/img_3.png",
    "static/img/img_4.png",
    "static/img/img_5.png",
    "static/img/img_6.png",
    "static/img/img_7.png",
    "static/img/img_8.png",
]



@app.route("/")
def index():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html',trending_products=trending_products.head(8),truncate = truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price = random.choice(price))

#routes 
@app.route("/main")
def main():
    return render_template('main.html')

@app.route("/index")
def indexredirect():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html',trending_products=trending_products.head(8),truncate = truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price = random.choice(price))

@app.route("/signup", methods=['POST', 'GET'])
def signup_route():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_signup = signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html',trending_products=trending_products.head(8),truncate = truncate,
                            random_product_image_urls=random_product_image_urls,
                            random_price = random.choice(price),
                            signup_message = 'User signed up successfully!')

@app.route("/signin", methods=['POST', 'GET'])
def signin_route():
    if request.method == "POST":
        username = request.form['signinUsername']
        password = request.form['signinPassword']

        new_signin = signin(username=username, password=password)
        db.session.add(new_signin)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html',trending_products=trending_products.head(8),truncate = truncate,
                            random_product_image_urls=random_product_image_urls,
                            random_price = random.choice(price),
                            signup_message = 'User signed in successfully!')



if __name__ == '__main__':
    app.run(debug=True)