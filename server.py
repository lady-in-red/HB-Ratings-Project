"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, jsonify, redirect, flash, session, request)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/users')
def user_list():
    """Show list of Users"""

    users_all = User.query.all()
    return render_template('user_list.html', users=users_all)


@app.route('/register', methods=['GET'])
def register_user():
    """Shows a login for user with a form"""

    return render_template('register_form.html')


@app.route('/get_reg', methods=["POST"])
def input_user_reg():
    """Adds user to db"""

    # grabbing form data
    user_email = request.form.get('user_email')
    user_pass = request.form.get('user_password')
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/")


    # is user in db?
    if not User.query.filter_by(email=user_email).first():
        user = User(email=user_email, password=user_pass)
        db.session.add(user)
        db.session.commit()
        flash('You have registered!')
    else:
        if User.query.filter_by(password=user_pass).first():
            session['user_email'] = user_email
            flash('You have registered before, but we\'ll log you in!')
        else:
            flash('Oops, try again!')
            return redirect('/registration_form')
        # grab user_id + add it to session
            # add userId to session
    ### added session
    session['user_email'] = user_email

    return redirect('/')




@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)

### added route that redirects to homepage with flash message
@app.route('/log_out')
def logging_out():
    """ Logs the user out once clicked"""

    session.clear()
    flash('You have logged out.')

    return redirect('/')


@app.route('/users/<int:user_id>')
def show_user_data(user_id):
    """Retrun page showing user data, including ratings"""

    user = User.query.get(user_id)

    return render_template('/user_page.html', user=user)



@app.route("/movies/<int:movie_id>", methods=['GET'])
def movie_detail(movie_id):
    """Show info about movie.

    If a user is logged in, let them add/edit a rating.
    """

    movie = Movie.query.get(movie_id)

    user_id = session.get("user_id")

    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    return render_template("movie.html",
                           movie=movie,
                           user_rating=user_rating)


@app.route("/movies/<int:movie_id>", methods=['POST'])
def movie_detail_process(movie_id):
    """Add/edit a rating."""

    # Get form variables
    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    if rating:
        rating.score = score
        flash("Rating updated.")

    else:
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        flash("Rating added.")
        db.session.add(rating)

    db.session.commit()

    return redirect("/movies/%s" % movie_id)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
