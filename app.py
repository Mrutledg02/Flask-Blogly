"""Blogly application."""
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Secret key for DebugToolbar
app.config['SECRET_KEY'] = "oh_so_secret"

# Initialize DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

# Redirect to list of users
@app.route('/')
def redirect_to_users():
    """Redirect to list of users."""
    return redirect('/users')

# Show all users
@app.route('/users')
def show_all_users():
    """Show all users."""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_listing.html', users=users)

# Show an add form for users
@app.route('/users/new', methods=['GET'])
def show_add_user_form():
    return render_template('new_user_form.html')

# Process the add form, adding a new user and going back to /users
@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Add new user and redirect to list of users."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

# Show information about the given user
@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

# Show the edit page for a user
@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_user_form(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

# Process the edit form, returning the user to the /users page
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.commit()
    return redirect('/users')

# Delete the user
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

if __name__ == '__main__':
    if app.config['ENV'] == 'development':
        app.run(debug=True)
    else:
        app.run()