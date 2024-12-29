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

        db.session.add(new_course)
        db.session.commit()

        return redirect(url_for('course'))  # Redirect to the courses page

    d_courses= draft_course()
    p_course = published_course()
    courses= index_course()
    return render_template('course.html',
                           user=current_user,
                           d_courses= d_courses,
                           p_courses=p_course,
                           courses= courses)

@app.route('/course/<course_id>', methods=["GET", 'POST'])
@login_required
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
