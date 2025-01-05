import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, ANY
from app import app, db
from app.models.user import User, PendingUser
from app.utils.user import (
    add_pending,
    cleanup_expired_pending_users,
    generate_verification_token,
    confirm_verification_token,
    send_verification_email,
)

class TestUserWorkflow(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['SERVER_NAME'] = 'localhost:5000'  # Fix for url_for
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_pending_user(self):
        pending_user = PendingUser(
            email="pendinguser@example.com",
            username="pendinguser",
            password="securepassword",
            first_name="John",
            last_name="Doe",
            dob="2000-01-01",
            role="Student",
        )
        with app.app_context():
            result = add_pending(pending_user)
            self.assertTrue(result)
            saved_user = PendingUser.query.filter_by(email="pendinguser@example.com").first()
            self.assertIsNotNone(saved_user)

    def test_pending_to_verified_user_promotion(self):
        pending_user = PendingUser(
            email="verifyuser@example.com",
            username="verifyuser",
            password="securepassword",
            first_name="Jane",
            last_name="Smith",
            dob="1990-05-15",
            role="Teacher",
        )
        with app.app_context():
            add_pending(pending_user)
            token = generate_verification_token(pending_user.email)
            verified_email = confirm_verification_token(token)
            self.assertEqual(verified_email, pending_user.email)
            new_user = User(
                email=pending_user.email,
                username=pending_user.username,
                password=pending_user.password,
                first_name=pending_user.first_name,
                last_name=pending_user.last_name,
                dob=pending_user.dob,
                role=pending_user.role,
                is_verified=True,
            )
            db.session.add(new_user)
            db.session.delete(pending_user)
            db.session.commit()
            verified_user = User.query.filter_by(email="verifyuser@example.com").first()
            self.assertIsNotNone(verified_user)
            self.assertTrue(verified_user.is_verified)

    @patch('app.utils.user.url_for')  # Mock url_for to avoid RuntimeError
    @patch('app.mail.send')  # Mock Flask-Mail's send method
    def test_send_verification_email(self, mock_mail_send, mock_url_for):
        mock_url_for.return_value = "http://example.com/verify"
        user = User(email="testuser@example.com", username="testuser")
        with app.app_context():
            send_verification_email(user)
        mock_mail_send.assert_called_once()
        mock_url_for.assert_called_once_with('verify_email', token=ANY, _external=True)

    def test_cleanup_expired_pending_users(self):
        expired_user = PendingUser(
            email="expired@example.com",
            created_at=datetime.utcnow() - timedelta(hours=25),
            username="expireduser",
            password="expiredpassword",
            first_name="Old",
            last_name="User",
            dob="1990-01-01",
            role="Student",
        )
        valid_user = PendingUser(
            email="valid@example.com",
            created_at=datetime.utcnow() - timedelta(hours=23),
            username="validuser",
            password="validpassword",
            first_name="Valid",
            last_name="User",
            dob="2000-01-01",
            role="Teacher",
        )
        with app.app_context():
            db.session.add(expired_user)
            db.session.add(valid_user)
            db.session.commit()
            cleanup_expired_pending_users()
            self.assertIsNone(PendingUser.query.filter_by(email="expired@example.com").first())
            self.assertIsNotNone(PendingUser.query.filter_by(email="valid@example.com").first())

if __name__ == "__main__":
    unittest.main()
