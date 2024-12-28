#!/usr/bin/env python3
"""
this is goung to handle some essentials needed by the course
"""
from app import app, db
from flask import redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from app.models.user import User
from app.models.course import *


def index_course():
    # If the user is not logged in, return all published courses
    courses = Courses.query.filter_by(status="Published").all()
    return courses

def published_course():
    """
    this retreves a published course for a teacher
    """
    if current_user.is_authenticated:
        # Query for courses with status 'draft' taught by the current user
        courses = Courses.query.filter_by(teacher_id=current_user.id, status='Published').all()
        return courses


def draft_course():
    """
    this fetches the draft course of the teacher
    """
    if current_user.is_authenticated:
        # Query for courses with status 'draft' taught by the current user
        courses = Courses.query.filter_by(teacher_id=current_user.id, status='Draft').all()
        return courses


def get_modules(course_id):
    # Fetch modules and their associated units in one query to avoid N+1 queries
    # modules = Modules.query.options(db.joinedload(Modules.units)).filter_by(course_id=course_id).all()
    modules= Modules.query.filter_by(course_id=course_id)
    return modules

def get_unit(module_id):
    units = Units.query.filter_by(module_id=module_id).all()
    return units