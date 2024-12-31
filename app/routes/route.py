#!/usr/bin/env python3
"""
this module is going to contain all my routes
"""
from datetime import datetime
from app import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.user import User, add_new_user, set_username, send_verification_email
from app.models.user import  PendingUser
from app.utils.user import  confirm_verification_token, add_pending
from app.routes.dashboard import *
from app.utils.course import *


@app.route('/')
@app.route('/index')
def index():
    """
    this function calls the index page of the website
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        courses= index_course()
        return render_template('index.html', courses= courses)


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Student':
        return redirect(url_for('student_dashboard'))
    else:
        return redirect(url_for("teacher_dashboard"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Collect and validate input
        first_name = request.form.get('first_name', "").strip()
        middle_name = request.form.get('middle_name', "").strip()
        last_name = request.form.get('last_name', "").strip()
        email = request.form.get('email', "").strip().lower()
        dob = request.form.get('dob', "").strip()
        password = request.form.get('password', "").strip()
        role = request.form.get('role')

        # Basic input validation
        if not all([first_name, last_name, email, password, dob]):
            flash("All fields are required.")
            return redirect(url_for("signup"))
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')  # Validate DOB format
            dob_long_format = dob_date.strftime('%B %d, %Y')
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.")
            return redirect(url_for("signup"))

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("user_exist1.html", email=existing_user.email)

        # Check if the user is already pending verification
        pending_user = PendingUser.query.filter_by(email=email).first()
        if pending_user:
            return render_template(
                'user_exist2.html',
                email=pending_user.email,
                verify=send_verification_email(pending_user)
            )
        # Create a username and hash the password
        username = set_username(first_name.capitalize(), middle_name.capitalize(), last_name.capitalize())
        hashed_password = generate_password_hash(password)

        # Create PendingUser and save to DB
        new_pending_user = PendingUser(
            username=username,
            email=email,
            password=hashed_password,
            first_name=first_name.capitalize(),
            middle_name=middle_name.capitalize(),
            last_name=last_name.capitalize(),
            dob=dob_long_format,
            role=role
        )
        if not add_pending(new_pending_user):
            flash("Error during signup. Please try again later.")
            return redirect(url_for("signup"))

        # Send email for verification
        send_verification_email(new_pending_user)
        flash("Signup successful! A verification email has been sent.")
        return render_template('next.html')

    return render_template('signup.html')


@app.route('/verify/<token>')
def verify_email(token):
    # Confirm token validity
    email = confirm_verification_token(token)
    if email is None:
        flash("Verification link is invalid or has expired.")
        return redirect(url_for("signup"))

    # Locate PendingUser and migrate to User table
    pending_user = PendingUser.query.filter_by(email=email).first()
    if not pending_user:
        flash("No pending user found for this email. Please sign up again.")
        return redirect(url_for("signup"))

    new_user = User(
        username=pending_user.username,
        email=pending_user.email,
        password=pending_user.password,
        first_name=pending_user.first_name,
        middle_name=pending_user.middle_name,
        last_name=pending_user.last_name,
        dob=pending_user.dob,
        is_verified=True,  # Mark as verified
        role=pending_user.role
    )
    if add_new_user(new_user):
        db.session.delete(pending_user)  # Cleanup PendingUser record
        db.session.commit()
        flash("Your account has been verified! Please log in.")
        return redirect(url_for("login"))
    else:
        flash("Error occurred during verification. Please try again.")
        return redirect(url_for("signup"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                flash('Please verify your email before logging in.')
                return redirect(url_for('login'))
            login_user(user)
            flash(f'successful login {user.last_name}', 'success')
            return redirect(url_for('dashboard'))
        elif not user:
            flash('User does not exist. Please sign up.')
            return redirect(url_for('signup'))
        else:
            flash('Incorrect password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/change_password')
def change_password():
    return "Still under implementation"

@app.route('/logout')
def logout():
    """This function logs the user out"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/<user_id>/profile')
@login_required
def Profile(user_id):
    """
    Displays the profile of the user with the given user_id.
    """
    # Fetch the user from the database
    user = User.query.get(user_id)

    if not user:
        flash("User not found.")
        return redirect(url_for('index'))

    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        # Get updated user data from the form
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')

        # Handle profile photo upload
        photo_file = request.files.get('photo')
        if photo_file and allowed_file(photo_file.filename):
            filename = secure_filename(photo_file.filename)
            photo_path = filename  # Just save the filename, not the full absolute path
            photo_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            photo_path = current_user.photo  # Keep the current photo if no new photo is uploaded

        # Update user information in the database
        current_user.first_name = first_name
        current_user.middle_name = middle_name
        current_user.last_name = last_name
        current_user.dob = dob
        current_user.photo = photo_path  # Update photo path if a new photo was uploaded
        current_user.updated_at = datetime.utcnow()  # Update the timestamp

        # Commit the changes
        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('Profile', user_id=current_user.id))  # Redirect to profile page after update

    # Render the form with the current user's details
    return render_template('edit_proofile.html', user=current_user)
