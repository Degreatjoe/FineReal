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
    if current_user.is_authenticated:  # Check if the user is logged in
        if current_user.role == 'Teacher':
            # Get courses taught by the teacher, filter by 'Published' status
            courses = current_user.courses_taught
        else:
            # Get courses the user is enrolled in, filter by 'Published' status
            courses = current_user.enrolled_courses
    else:
        # If the user is not logged in, return all published courses
        courses = Course.query.filter_by(status="Published").all()
        
    return courses

def published_course():
    """
    this retreves a published course for a teacher
    """
    if current_user.is_authenticated:
        # Query for courses with status 'draft' taught by the current user
        courses = Course.query.filter_by(teacher_id=current_user.id, status='Published').all()
        return courses


def draft_course():
    """
    this fetches the draft course of the teacher
    """
    if current_user.is_authenticated:
        # Query for courses with status 'draft' taught by the current user
        courses = Course.query.filter_by(teacher_id=current_user.id, status='Draft').all()
        return courses
