import re
from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Home Page - Will show list of users"""
    return redirect("/users")


@app.route("/users")
def all_users():
    """Will Show List of All Users in DB"""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Display Form to Add User"""
    return render_template('new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle Form Submission for new User"""
    # create new user from form data
    new_user = User(
        first_name=request.form['fname'],
        last_name=request.form['lname'],
        image_url=request.form['iurl'] or None)
    # add user to db and commit
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Display User Information"""
    user = User.query.get_or_404(user_id)
    return render_template("userprofile.html", user=user)


@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    """Display Form to Edit user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_modify(user_id):
    """Handle form submission for modifying user"""
    # get data from user input
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['iurl']
    # update user in DB and commit
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""
    # get userid and delete from DB
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
