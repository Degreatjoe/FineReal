#!/usr/bin/python3
"""
this file contains the routes related to coures
"""
from app import app, db
from flask import redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from app.models.user import User
from app.models.course import *
from app.utils.course import *


@app.route('/course', methods=['GET', 'POST'])
@login_required
def course():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form.get('category', '')
        difficulty = request.form.get('difficulty', 'Beginner')
        prerequisite = request.form.get('prerequisite', '')
        status = request.form.get('status', 'Draft')
        teacher_id = current_user.id

        new_course = Course(
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

@app.route('/course/<course_id>', methods=["GET", "POST"])
@login_required
def course_view( course_id):
    if request.method == "POST":
        title = request.form.get("title")
        course_id = course_id
        new_module = Module(title = title, course_id=course_id)
        db.session.add(new_module)
        db.session.commit()
        return redirect(url_for('course_view', course_id=course_id))

    v_course =  Course.query.get(course_id)
    modules= get_module(course_id=course_id)
    return render_template("course_view.html", course=v_course, user=current_user, modules= modules)

@app.route('/<course_id>/models/', methods=["GET", "POST"])
def model_view():
    pass
