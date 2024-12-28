#!/usr/bin/env python3
"""
this is the file that runs the auth app
you run the app by executing './run.py'
"""
from app import app
from app import db


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)