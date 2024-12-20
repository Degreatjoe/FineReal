# models/user.py
from app import db, login_manager
from flask_login import UserMixin
from app.models.base import BaseModel

class User(BaseModel, db.Model, UserMixin):
    __tablename__ = 'users'

    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    dob = db.Column(db.String)
    role = db.Column(db.String, nullable=False)

    # Relationships
    courses_taught = db.relationship('Course', backref='teacher', lazy=True)
    enrolled_courses = db.relationship('Enrollment', backref='student', lazy=True)

    def __repr__(self):
        return f'<User  {self.username}>'

# Import Course here to avoid circular imports
from app.models.course import Course

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)# PendingUser class and other functions...

class PendingUser(BaseModel, db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)