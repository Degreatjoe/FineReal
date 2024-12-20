#!/usr/bin/python3
"""
This file contains the modules for course management.
"""
from app.models.base import BaseModel, db

# Import User here to avoid circular import
def get_user():
    from app.models.user import User
    return User

class Course(BaseModel, db.Model):
    __tablename__ = 'courses'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60))
    difficulty = db.Column(db.String(60), default="Beginner")
    prerequisite = db.Column(db.Text)
    status = db.Column(db.String(60))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    modules = db.relationship('Module', backref='course', lazy=True)
    enrolled_students = db.relationship('Enrollment', backref='course', lazy=True)

# Define other models like Module, Unit, Enrollment...

class Module(BaseModel, db.Model):
    __tablename__ = 'modules'
    
    title = db.Column(db.String(60), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    # One-to-many relationship to units
    units = db.relationship('Unit', backref='module', lazy=True)


class Unit(BaseModel, db.Model):
    __tablename__ = 'units'
    
    content_type = db.Column(db.String(50))  # You might want to define a fixed set of content types
    content_data = db.Column(db.Text)  # Changed to db.Text for storing larger content

    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)


class Enrollment(BaseModel, db.Model):
    __tablename__ = 'enrollments'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
