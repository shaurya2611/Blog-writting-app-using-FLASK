from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Opening and reading the json file.
with open('config.json', 'r') as jsonfile:
    params = json.load(jsonfile)["params"]

# Creating a Flask application object
app = Flask(__name__)
app.secret_key = 'secret-key'
local_server = True

# adding DATABASE to flask app
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

# Creating an object of SQLAlchemy class with application object as the parameter.
db = SQLAlchemy(app)


@app.route("/index")
def home():
    return render_template('index.html', params=params)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    number = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    msg = db.Column(db.String(100), unique=False, nullable=True)
    date = db.Column(db.String(12), unique=False, nullable=False)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to database'''

        # fetching values from the form filled by user
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('msg')
        phone = request.form.get('number')

        # storing the fetched data from form during run time to the database
        entry = Contacts(name=name, email=email, msg=message, number=phone, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    slug = db.Column(db.String(25), unique=True, nullable=False)
    content = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=False)
    blogger = db.Column(db.String(25), unique=True, nullable=False)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    # query to connect to sql_alchemy database
    fetched_post = Posts.query.filter_by(slug=post_slug).first()
    # returning the fetched "post" from DB to the frontend
    return render_template('post.html', params=params, post=fetched_post)


@app.route("/dashboard", methods=['GET', 'POST'])
def dash():
    # Before starting session dont forget to set the secret key
    # Checking in casae user is already logged in
    if 'users' in session and session['users'] == 'shaurya@singh':
        # If user is logged he mush able to see all the post with edit and delete options
        # Fetching data from the Posts Table by executing below query
        posts_db = Posts.query.all()
        # passing 'params' from config.json and 'post' query results from DB to dashboard.html
        return render_template('dashboard.html', params=params, posts=posts_db)

    # In case of post request
    if request.method == 'POST':

        # getting the entered user and password from frontend
        user_mail = request.form.get('email')
        password = request.form.get('password')

        if user_mail == 'shaurya@singh' and password == '123456':

            # Starting SESSION in case user is authenticated
            session['users'] = user_mail
            post = Posts.query.all()
            return render_template('dashboard.html', params=params,post=post)
        else:
            return render_template('login.html', params=params)

    # In case of GET(default one) request
    else:
        return render_template('login.html', params=params)


@app.route("/edit/<string : sno>" , methds=['GET','POST'])
def post_edit(sno):
    # If User is logged in only then EDIT is allowed
    if 'users' in session and session['users'] == 'shaurya@singh':




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
