#!/usr/bin/env python3
import unittest
from app import app, db
from unittest.mock import patch


class TestRoutes(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()

        # Initialize the database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('app.routes.route.send_verification_email')  # Mock send_verification_email function
    def test_signup_success(self, mock_send_email):
        # Mock the send_verification_email so no email is actually sent
        mock_send_email.return_value = None

        response = self.client.post('/signup', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'dob': '2000-01-01',
            'password': 'password123',
            'role': 'Student',
        })

        self.assertEqual(response.status_code, 200)  # Check for success
        # location would be none because its trying to send a mail
        self.assertEqual(response.location, None)  

    def test_signup_missing_email(self):
        response = self.client.post('/signup', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
            'dob': '2000-01-01',
            'password': 'password123',
            'role': 'Student',
        })
        self.assertEqual(response.status_code, 302)
