import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///moviematch.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        try:
            id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                            request.form.get("username"),
                            generate_password_hash(request.form.get("password")))
        except ValueError:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")

@app.route("/form", methods=["GET", "POST"])
@login_required
def form():
    directors = db.execute("SELECT DISTINCT(Director) FROM movies ORDER BY Director")
    actors = db.execute("SELECT DISTINCT(Star1) FROM movies ORDER BY Star1")
    if request.method == "POST":
        # Validate form submission
        genre = request.form.get("genre")
        director = request.form.get("director")
        actor = request.form.get("actor")
        minyear = request.form.get("minyear")
        maxyear = request.form.get("maxyear")
        minrating = request.form.get("minrating")
        maxrating = request.form.get("maxrating")
        if genre is None and director is None and actor is None and maxyear == "1919" and minrating == "7.5" and maxrating == "7.5":
            return apology("change at least one field to product results")
        if not genre:
            genre = None
        if not director:
            director = None
        if not actor:
            actor = None
        if minyear == "1919":
            minyear = "1920"
        if maxyear == "1919":
            maxyear = "2020"
        if minrating == "7.5":
            minrating = "7.6"
        if maxrating == "7.5":
            maxrating = "9.3"
        db.execute("INSERT INTO form (minrating, maxrating, director, genre, actor, minyear, maxyear, user_id) VALUES (:minrating, :maxrating, :director, :genre, :actor, :minyear, :maxyear, :user_id)", minrating=minrating, maxrating=maxrating, director=director, genre=genre, actor=actor, minyear=minyear, maxyear=maxyear, user_id=session["user_id"])
        return redirect("/results")
    else:
        return render_template("form.html", directors = directors, actors = actors)

@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    if request.method == "GET":
        submission = db.execute("SELECT * FROM form WHERE user_id = ? ORDER BY id DESC", session["user_id"])
        if submission[0]['genre'] is not None:
            sub_genre = "%"+submission[0]['genre']+"%"
        else:
            sub_genre = submission[0]['genre']
        mov_results = db.execute("SELECT Series_Title, Runtime, Genre, IMDB_Rating, Released_Year, Director FROM movies WHERE (IMDB_Rating >= ? OR ? IS NULL) AND (IMDB_Rating <= ? OR ? IS NULL) AND (Director LIKE ? OR ? IS NULL) AND (Genre LIKE ? OR ? IS NULL) AND (Star1 LIKE ? OR Star2 LIKE ? OR Star3 LIKE ? OR Star4 LIKE ? OR ? IS NULL) AND (Released_Year >= ? OR ? IS NULL) AND (Released_Year <= ? OR ? IS NULL)", submission[0]['minrating'], submission[0]['minrating'], submission[0]['maxrating'], submission[0]['maxrating'], submission[0]['director'], submission[0]['director'], sub_genre, sub_genre, submission[0]['actor'], submission[0]['actor'], submission[0]['actor'], submission[0]['actor'], submission[0]['actor'], submission[0]['minyear'], submission[0]['minyear'], submission[0]['maxyear'], submission[0]['maxyear'])
        for i in range(0, len(mov_results)):
            db.execute("INSERT INTO results (movie_name, runtime, genre, rating, released_year, user_id, director) VALUES (?, ?, ?, ?, ?, ?, ?)", mov_results[i]['Series_Title'], mov_results[i]['Runtime'], mov_results[i]['Genre'], mov_results[i]['IMDB_Rating'], mov_results[i]['Released_Year'], session["user_id"], mov_results[i]['Director'])
        results = db.execute("SELECT * FROM results")
        return render_template("results.html", results=results)
    #else - start here

""" @app.route("/watched")
@login_required
def watched():

    return render_template("watched.html") """