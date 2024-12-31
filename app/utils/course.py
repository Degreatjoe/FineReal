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

def available_courses(user_id):
    """
    Fetches courses that are published and not enrolled by the current user.
    :param user_id: ID of the current user (student)
    :return: List of courses that the user is not enrolled in
    """
    # Fetch all published courses
    all_courses = Courses.query.filter_by(status="Published").all()
    
    # Get the list of courses the user is enrolled in
    enrolled_courses = get_courses_by_student(user_id)
    
    # Filter out courses that the user is already enrolled in
    available_courses = [course for course in all_courses if course not in enrolled_courses]
    
    return available_courses

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

def get_students_by_teacher(teacher_id):
    """
    Function to fetch all students enrolled in courses created by a specific teacher.
    :param teacher_id: ID of the teacher
    :return: List of student User objects enrolled in the teacher's courses
    """
    # Fetch all courses created by the teacher
    courses = Courses.query.filter_by(teacher_id=teacher_id).all()
    
    # Initialize an empty list to store students
    students = set()
    
    # For each course created by the teacher, fetch the students (enrolled users)
    for course in courses:
        # Fetch the enrollments for the course
        enrollments = Enrollments.query.filter_by(course_id=course.id).all()
        
        # Extract the students from the enrollments
        for enrollment in enrollments:
            students.add(enrollment.user)
    
    return list(students)

def get_courses_by_student(user_id):
    """
    Function to fetch all courses a student is enrolled in.
    :param user_id: ID of the student
    :return: List of course objects the student is enrolled in
    """
    # Fetch the enrollments for the user (student)
    enrollments = Enrollments.query.filter_by(user_id=user_id).all()
    
    # Extract the courses from the enrollments
    courses = {enrollment.courses for enrollment in enrollments}
    
    return list(courses)

def get_students_by_course(course_id):
    """
    Function to fetch all students enrolled in a course.
    :param course_id: ID of the course
    :return: List of student User objects enrolled in the course
    """
    # Fetch the enrollments for the course
    enrollments = Enrollments.query.filter_by(course_id=course_id).all()
    
    # Extract the students from the enrollments
    students = [enrollment.user for enrollment in enrollments]
    
    return students

def is_user_enrolled_in_course(user_id, course_id):
    """
    Check if a user is enrolled in a specific course.
    
    :param user_id: ID of the user
    :param course_id: ID of the course
    :return: True if the user is enrolled in the course, False otherwise
    """
    # Query the Enrollments table to check if the user is enrolled in the course
    enrollment = Enrollments.query.filter_by(user_id=user_id, course_id=course_id).first()
    
    # Return True if the enrollment exists, otherwise False
    return enrollment is not None

