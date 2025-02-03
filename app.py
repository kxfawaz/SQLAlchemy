from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Post , Tag, PostTag # Import User class explicitly
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



@app.route('/users/<int:user_id>/posts/new')
def handle_newpost(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts_new.html', user=user,tags=tags)
    
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_new(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user,
        tags=tags
    )
    
    db.session.add(new_post)
    db.session.commit()
   

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags= Tag.query.all()
    return render_template('posts_show.html', post=post,tags=tags)
    
    
@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts_edit.html', post=post,tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()


    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_delete(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('all_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)


@app.route('/tags/new')
def new_tag():
    return render_template('tag_new.html')
    
@app.route('/tags/new', methods=["POST"])
def process_tag():
   new_tag = Tag(name=request.form['name'])
   db.session.add(new_tag)
   db.session.commit()
   return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag=tag,)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def process_edit(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()
    
    return redirect("/tags")
    
    

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit() 
    
    return redirect("/tags")    