#!/usr/bin/env python3
"""
this file contains the routes related to coures
"""
from app import app, db, allowed_file
from flask import redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.models.course import *
from app.utils.course import *
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory, current_app


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/units/<course_id>/<module_id>', methods=["GET", "POST"])
@login_required
def add_unit(course_id, module_id):
    if request.method == "POST":
        if current_user.is_authenticated:
            title = request.form.get('title')
            content_type = request.form.get('content_type')
            module_id = request.form.get('id')  # Get the module ID from the form

            # Handle the content data based on content type
            content_data = None

            if content_type == 'page':
                content_data = request.form.get('content')  # Text content for "Page"

            elif content_type == 'video':
                video_file = request.files.get('video_file')  # Get the uploaded video file
                if video_file and allowed_file(video_file.filename):
                    filename = secure_filename(video_file.filename)  # Secure the filename
                    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    # Check if the directory exists, create it if not
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])

                    video_file.save(video_path)  # Save the video to the upload folder
                    content_data = video_path  # Store the file path of the uploaded video

            # Create and save the new unit
            new_unit = Units(
                title=title,
                content_type=content_type,
                content_data=content_data,  # Store the content data (either text or video path)
                module_id=module_id
            )
            new_unit.save()
            print("Successfully added!")

            return redirect(url_for('course_view', course_id=course_id))
        else:
            return "Not Authorized"
    units= get_unit(module_id=module_id)
    return render_template("units.html", units=units)

@app.route('/delete_units', methods=['POST'])
def delete_units():
    # Get the list of unit IDs from the request
    data = request.get_json()
    unit_ids = data.get('units')

    # Validate the input
    if not unit_ids or not isinstance(unit_ids, list):
        return jsonify({'success': False, 'message': 'Invalid or missing unit IDs.'}), 400

    try:
        # Deleting units from the database
        units_to_delete = Units.query.filter(Units.id.in_(unit_ids)).all()
        for unit in units_to_delete:
            db.session.delete(unit)
        
        db.session.commit()  # Commit the deletion to the database

        return jsonify({'success': True, 'message': 'Units deleted successfully.'})
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({'success': False, 'message': f'Error deleting units: {str(e)}'}), 500

@app.route('/content_page/<unit_id>', methods=["GET", "POST"])
@login_required
def content_page(unit_id):
    
    unit= Units.query.get_or_404(unit_id)

    # Get the module related to the unit, and then get the course related to that module
    courses = unit.module.course  # Access the related course through the module

    return render_template("content.html", unit=unit, course=courses, user=current_user)

@app.route('/add_content/<unit_id>', methods=["GET", "POST"])
@login_required
def add_content(unit_id):
    unit= Units.query.get_or_404(unit_id)

    if request.method == "POST":
        # Get the updated content from the form
        content_data = request.form.get('content_data')  # For "page" content type

        # Update the unit's attributes
        unit.content_data = content_data

        # Commit the changes to the database
        db.session.commit()
        print('content data updated')
        return redirect(url_for('content_page', unit_id= unit_id))
    return render_template('page.html', unit = unit, user=current_user)

