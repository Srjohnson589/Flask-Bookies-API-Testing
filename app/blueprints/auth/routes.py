from . import auth
from .forms import LoginInput, SignUpInput
from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user,logout_user, login_required
from werkzeug.security import check_password_hash
from app.models import User


# Login route
@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginInput()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        queried_user = User.query.filter(User.name == username).first()
        if queried_user and check_password_hash(queried_user.password, password):
            flash(f'Success! Welcome {username}, you have logged in.', 'success')
            login_user(queried_user)
            return redirect(url_for('pokesearch.home'))
        else:
            flash('Invalid name or password', 'danger')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

# Logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Signup route
@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpInput()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        queried_user = User.query.filter(User.username == username).first()
        if queried_user:
            flash('A user with that name already exists. Try adding an initial or two!', 'danger')
            return render_template('signup.html', form=form)
        
        new_user = User(name, password)
        new_user.save()
        flash('Success! Thank you for signing up!', 'success')
        return redirect(url_for('auth.login'))
        
    else:
        return render_template('signup.html', form=form)
