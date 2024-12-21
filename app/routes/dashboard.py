#!/usr/bin/python3
"""
This contains the routes for the teacher's dashboard.
"""
from app import app
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.routes.course import *
from app.utils.course import *

@app.route('/dashboard/teacher')
@login_required
def teacher_dashboard():
    """
    This displays the teacher's dashboard.
    """
    d_courses= draft_course()
    return render_template('tdashboard.html', user=current_user, d_courses= d_courses)

@app.route('/students')
def students():
    """
    This fetches and displays all students enrolled in the teacher's courses.
    """
    # Placeholder list of students
    students_list = [
        {'id': 1, 'name': 'Student One'},
        {'id': 2, 'name': 'Student Two'},
        {'id': 3, 'name': 'Student Three'},
    ]
    return render_template('students.html', students=students_list)

@app.route('/assignments')
def assignments():
    """
    This fetches and displays all assignments created by the teacher.
    """
    # Placeholder list of assignments
    assignments_list = [
        {'id': 1, 'title': 'Assignment 1', 'due_date': '2023-10-15'},
        {'id': 2, 'title': 'Assignment 2', 'due_date': '2023-10-20'},
    ]
    return render_template('assignments.html', assignments=assignments_list)

@app.route('/analytics')
def analytics():
    """
    This displays analytics related to the teacher's courses and students.
    """
    # Placeholder for analytics data
    analytics_data = {
        'total_courses': 5,
        'total_students': 30,
        'average_grade': 85,
    }
    return render_template('analytics.html', analytics=analytics_data)

@app.route('/settings')
def settings():
    """
    This allows the teacher to update their profile and settings.
    """
    return render_template('settings.html')

# Add more routes as needed for additional 


@app.route('/dashboard/student')
@login_required
def student_dashboard():
    """
    this returns the student dashboard
    """
    p_courses = index_course()
    return render_template('sdashboard.html', user=current_user, p_courses= p_courses)