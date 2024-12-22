#!/usr/bin/python3
"""
this file contains all misceleneous functions neede for
the user authentication
"""
from app import app, db, mail
from itsdangerous import URLSafeTimedSerializer
from app.models.user import User, PendingUser
from flask_mail import Message
from flask import url_for, render_template
from datetime import datetime, timedelta



def add_new_user(user):
    """
    This function receives a user instance and saves it to the database.
    
    Parameters:
        user (User): The user instance to be saved.
    
    Returns:
        bool: True if the user was successfully saved, False otherwise.
    """
    if not isinstance(user, User):
        print("Invalid user instance.")
        return False

    try:
        db.session.add(user)
        db.session.commit()
        print(f"Account has been created for {user.username}")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred during registration: {e}")
        return False

def cleanup_expired_pending_users():
    expiration_time = datetime.utcnow() - timedelta(hours=24)  # 24-hour expiration
    expired_users = PendingUser.query.filter(PendingUser.created_at < expiration_time).all()
    if expired_users:
        for user in expired_users:
            print(f"Removing expired pending user: {user.email}")
            db.session.delete(user)
        db.session.commit()

def add_pending(pending_user):
    """
    creating a pending user
    """
    if not isinstance(pending_user, PendingUser):
        print("Invalid user instance.")
        return False
    try:
        db.session.add(pending_user)
        db.session.commit()
        print(f"Account has been created for {pending_user.username}")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred during registration: {e}")
        return False


def set_username(first_name, middle_name, last_name):
    """
    this function sets the username (implementiung the facebook username pattern)
    from the input of the user during the registration of
    an account.

    it checks if the user has a middle name:
    if they do it sets the username as "firstname middlename lastname"
    otherwise it sets the username as "firstname lastname"

    returns the username
    """
    if middle_name:
        username = f'{first_name} {middle_name} {last_name}'
    else:
        username = f"{first_name} {last_name}"
    return username

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification-salt')

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
    except Exception:
        return None
    return email

def send_verification_email(user):
    token = generate_verification_token(user.email)
    verify_url = url_for('verify_email', token=token, _external=True)
    msg = Message('Verify Your Email', recipients=[user.email])
    msg.body = f'Hi {user.username}, please verify your email by clicking on the following link: {verify_url}'
    msg.html = render_template(
        "verification.html",
        username=user.username,
        verification_link=verify_url,
        website="FINELEARN",
        support_email="[support_email]",
        year = datetime.now().year
    )
    mail.send(msg)
