#!/usr/bin/env python3
"""
this file contains the routes related to coures
"""
from app import app, db
from flask import redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from app.models.user import User
from app.models.course import *
from app.utils.course import *
from app.routes.unit import *


@app.route('/course', methods=['GET', 'POST'])
@login_required
def course():
    """
    this fuction displays the courses on the courses screen
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form.get('category', '')
        difficulty = request.form.get('difficulty', 'Beginner')
        prerequisite = request.form.get('prerequisite', '')
        status = request.form.get('status', 'Draft')
        teacher_id = current_user.id

        new_course = Courses(
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            prerequisite=prerequisite,
            status=status,
            teacher_id=teacher_id
        )

        new_course.save()

        return redirect(url_for('course'))  # Redirect to the courses page

    d_courses= draft_course()
    p_courses= published_course()
    a_courses= available_courses(current_user.id)
    courses= index_course()
    e_courses=get_courses_by_student(current_user.id)
    # Check if the current user is enrolled in each course
    enrolled_status = {}
    for course in courses:
        enrolled_status[course.id] = is_user_enrolled_in_course(current_user.id, course.id)

    print(enrolled_status)

    return render_template('course.html',
                           user=current_user,
                           d_courses= d_courses,
                           p_courses=p_courses,
                           a_courses=a_courses,
                           courses= courses,
                           e_courses=e_courses,
                           enrolled_status=enrolled_status)

@app.route('/course/<course_id>', methods=["GET", 'POST'])
def course_view(course_id):
    """
    Displays the course management screen for the given course ID.
    """
    if request.method == 'POST':
        title= request.form.get('title')
        courses_id = course_id
        if not title and not courses_id:
            print("All field must be filled!")
            flash("All fields must be filled!", "error")
            return redirect(url_for('course_view', course_id=course_id))
        new_module= Modules(title=title, course_id=course_id)
        new_module.save()
        print("successfully added!")
        return redirect(url_for('course_view', course_id=course_id))

    # Fetch the course
    v_course = Courses.query.get_or_404(course_id)
    modules = Modules.query.filter_by(course_id=course_id).all()

    return render_template(
        "course_view.html",
        course=v_course,
        user=current_user,
        modules=modules
    )

@app.route('/enroll/<course_id>')
@login_required
def enroll(course_id):
    if current_user.role == 'Student':
        course_id= course_id
        user_id = current_user.id
        new_enrollment = Enrollments(course_id=course_id, user_id=user_id)
        if new_enrollment:
            new_enrollment.save()
            flash(f'enrolled to the course {course_id}', 'success')
            return redirect(url_for('course'))
        else:
            flash('An error occured during the enrollment, please try again', 'error')
            return redirect(url_for('course'))
    else:
        flash('Only student can enroll to courses', 'error')
        return redirect(url_for('course'))
@app.route('/students')
def students():
    students = get_students_by_teacher(current_user.id)
    return render_template("students.html", students= students, user=current_user)

@app.route('/delete/<course_id>/<module_id>')
def delete_module(course_id, module_id):
    modules= Modules.query.get(module_id)
    if modules:
        if modules.units:
            for unit in modules.units:
                db.session.delete(unit)
        db.session.delete(modules)
        db.session.commit()
        return redirect(url_for('course_view', course_id=course_id))
    else:
        flash(f"couldn't delete the module {module_id}")
        return redirect(url_for('course_view', course_id=course_id))

@app.route('/toggle_course_status<course_id>')
def toggle_course_status(course_id):
    courses= Courses.query.get_or_404(course_id)
    if courses.status == 'Published':
        courses.status = 'Draft'
        db.session.commit()
        print(f'status changed to {courses.status}')
        flash(f"status changed to {courses.status}", "success")
        return redirect(url_for('course_view', course_id=course_id))
    else:
        courses.status = 'Published'
        db.session.commit()
        print(f'status changed to {courses.status}')
        flash(f"status changed to {courses.status}", "success")
        return redirect(url_for('course_view', course_id=course_id))
