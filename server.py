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


@app.route('/registration-form')
def register_user():
    """Creates a login for user"""

    return render_template('registration-form.html')


@app.route('/get-reg', methods=["POST"])
def input_user_reg():
    """Adds user to db"""

    # grabbing form data
    user_email = request.form.get('user_email')
    user_pass = request.form.get('user_password')

    # is user in db?
    if not User.query.filter_by(email=user_email).first():
        user_email = User(email=user_email, password=user_pass)
        db.session.add(user_email)
        db.session.commit()
        flash('You have registered!')
    else:
        flash('You have registered before, but we\'ll log you in!')
        # grab user_id + add it to session

    return redirect('/')

    # look in db to see if email + pass in db
    # IF not, add user data to db, grab db user_id, create session with that id
        # log in, flash homepage
    # IF grab db user_id and set session with that id as session[user_id] = 'boo')
        # flash Login successful
        # redirect to homepage

    #log out
        # remove session[user_id] from session
        # flash logged out
        # redirect to main page
    



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
