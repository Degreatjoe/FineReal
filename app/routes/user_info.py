#!/usr/bin/env python3
from datetime import datetime
from app import app, db
from flask import redirect, render_template, request, url_for, flash
from flask_login import  current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.user import User, add_new_user, set_username, send_verification_email
from app.models.user import  PendingUser
from app.utils.user import  confirm_verification_token, add_pending
from app.routes.dashboard import *
from app.utils.course import *


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

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = User.query.get(current_user.id)
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        # Check if current password matches the user's stored password
        if not check_password_hash(user.password, current_password):  # Assuming `check_password` is a method in the User model
            flash("Current password is incorrect", "error")
            return redirect(url_for('change_password'))
        
        # Hash the new password and update the user's password
        user.password = generate_password_hash(new_password)
        db.session.commit()
        
        flash("Your password has been updated successfully", "success")
        return redirect(url_for('Profile', user_id=current_user.id))
    return render_template('change_password.html', user=current_user)  # Use a template for the form

@app.route('/<usre_id>', methods=["DELETE"])
@login_required
def delete_user():
    user = User.query.get(current_user.id)

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            flash('Account Delete!')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"{str(e)}", 'error')
            return redirect(url_for('profile', current_user.id))

