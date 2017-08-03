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
    # user_id = user.user_id
    # age = user.age
    # zipcode = user.zipcode
    # user_ratings = user.ratings

    return render_template('/user_page.html', user=user)
    #                                           age=age,
    #                                           zipcode=zipcode,
    #                                           user_ratings=user_ratings)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
