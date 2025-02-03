from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User  # Import User class explicitly
from flask_debugtoolbar import DebugToolbarExtension

# Initialize Flask app
app = Flask(__name__)

# Configuration for SQLAlchemy and Debug Toolbar
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize DebugToolbar
debug = DebugToolbarExtension(app)

# Connect to the database
connect_db(app)  # Initialize the SQLAlchemy app connection

# Create all tables in the database (Make sure app context is active)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect("/users")

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route('/users/new', methods=["GET"])
def new_user():
    return render_template("users_new.html")


@app.route('/users/new', methods=["POST"])
def new_users():
    
    new_user = User(
    first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    image_url = request.form["image_url"] or None)
    

    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")
    
@app.route('/users/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users_details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template('edit.html')

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')
    
@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')
    