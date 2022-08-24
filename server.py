"""Server for movie ratings app."""

from crypt import methods
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """homepage"""

    return render_template("homepage.html")

@app.route("/movies")
def get_movies():
    """view all movies"""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies = movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie) 


@app.route("/movies/<movie_id>/review", methods=['POST'])
def give_review(movie_id):
    """"pass over user review and store the data in database called reviews """

    score = request.form.get("review")
    email = session.get("user_email")
    user = crud.get_user_by_email(email)
    movie = crud.get_movie_by_id(movie_id)

    new_review = crud.create_rating(user, movie, score)
    db.session.add(new_review)
    db.session.commit()

    return redirect("/movies/<movie_id>")



@app.route("/users")
def get_users():
    """view all users"""

    users = crud.get_users()

    return render_template("all_users.html", users = users)


@app.route("/user", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user: 
        flash("Cannot create an account with that email. Try again.")
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account was created successfully and you can now log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """show individual user"""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user = user)

@app.route("/login", methods=["POST"])
def process_login():
    """Process User Login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect. Please try again.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")






if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
