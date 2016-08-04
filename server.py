"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently and that is horrible. This line fixes this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)



@app.route('/login', methods=['GET'])
def user_login():

    return render_template("user_login.html")


@app.route('/confirm', methods=["POST"])
def checkdb():
    """Checks database for user email and password"""

    uemail = request.form.get("useremail")
    upassword = request.form.get("userpassword")

  # E will be an object if user email present in database and E will be None if not in db
    E = User.query.filter(User.email==uemail).first()
    P = User.query.filter(User.password==upassword).first()

    if E == None or P == None: 
        print "Please try again and enter a different email address!"
        return render_template("user_login.html")
    else: 
        db.session.commit() 
        return redirect ('/')


@app.route('/register', methods=['GET'])
def register_form():

    return render_template("register_input.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
