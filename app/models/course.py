#!/usr/bin/env python3
"""
This file contains the modules for course management.
"""
from app.models.base import BaseModel, db

# Import User here to avoid circular import
def get_user():
    from app.models.user import User
    return User

class Courses(BaseModel, db.Model):
    __tablename__ = 'courses'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60))
    difficulty = db.Column(db.String(60), default="Beginner")
    prerequisite = db.Column(db.Text)
    status = db.Column(db.String(60))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    modules = db.relationship('Modules', backref='courses', lazy=True)
    enrolled_students = db.relationship('Enrollments', backref='courses', lazy=True)

# Define other models like Module, Unit, Enrollment...

class Modules(BaseModel, db.Model):
    __tablename__ = 'modules'
    
    title = db.Column(db.String(60), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    # One-to-many relationship to units
    units = db.relationship('Units', backref='module', lazy=True)


class Units(BaseModel, db.Model):
    __tablename__ = 'units'
    
    title= db.Column(db.String(60))
    content_type = db.Column(db.String(50))
    content_data = db.Column(db.Text)

    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)


class Enrollments(BaseModel, db.Model):
    __tablename__ = 'enrollments'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
