"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie
from datetime import datetime

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session for it to be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""


    Movie.query.delete()

    for line in open("seed_data/u.item"):
        line = line.rstrip()
        line = line.split("|")[:5]
        print line
        movie_id, title, nodatetime_rel, video_rel, imdb_url = line
        # nodatetime_rel format is 01-Jan-1995 
        
        if nodatetime_rel:
            released_at = datetime.strptime(nodatetime_rel, "%d-%b-%Y") 
        #released_at looks like (1995, 1, 1)
        else:
            released_at = None 

        # takes out duplicative year from title
        title = title[:-7]

        film = Movie(movie_id=movie_id,
                     title=title, 
                     released_at=released_at,
                     imdb_url=imdb_url)

        db.session.add(film)

    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    Rating.query.delete()    #to prevent duplicate ratings

    for line in open("seed_data/u.data"):
        line = line.rstrip()
        line = line.split()
        print line
        user_id, movie_id, score, timestamp = line 

        single_rating = Rating(user_id=user_id,
                            movie_id=movie_id,
                            score=score)
        db.session.add(single_rating)
    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'nloew_id': max_id + 1})
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    # set_val_user_id()
