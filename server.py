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


@app.route('/login', methods=['GET'])
def user_login():

    return render_template("user_login.html")


@app.route('/confirm', methods=["POST"])
def checkdb():
    """Checks database for user email and password"""

    u_email = request.form.get("useremail")
    u_password = request.form.get("userpassword")

  # user will be a User object if user email present in database and E will be None if not in db
    user = User.query.filter(User.email==u_email).first()

    if user.password != u_password or not user: 
        return render_template("user_login.html")
    
    return redirect ('/users/{}'.format(user.user_id))


@app.route('/register', methods=['GET'])
def register_form():
    """Allows new users to register."""

    return render_template("register_input.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def users_page(user_id):
    """Once logged in, user can access their current ratings."""

    # user = User.query.filter(User.user_id==user_id).first()
    user_id_confirm = User.query.get(user_id)
    # score = user_id_confirm.score
    # age = user_id_confirm.age
    # zipcode = user_id_confirm.zipcode
    # film = user_id_confirm.film.all()
    return render_template("user_info.html", user=user_id_confirm)


@app.route('/movies')
def return_movie_list(film):
    """Returns a movie list."""

    film = Rating.query.all()
    return render_template("movie_list.html", film=film)


@app.route('/movies/<int:movie_id>')
def film_detail_page(movie_id):
    """Returns all the details about each film."""

    # query movie table for movie_id use .get
    # query rating table to get all ratings for that movie
    movie_ratings = Ratings.query.filter(movie_id == movie_id).all()
    # get movie information for our movie
    film_details = Movie.query.get(movie_id)

    cursor = db.session.execute(
        "SELECT * FROM movies")
    film_details = cursor.fetchall()
    db.session.commit()
    return render_template("movie_details.html", film_details=film_details)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
