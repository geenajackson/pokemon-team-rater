"""Tests related to User functionality."""

import os
#python debugger
import pdb
from unittest import TestCase

from models import db, User

# set database to a test database before importing app

os.environ['DATABASE_URL'] = "postgresql:///teamrater-test"

from app import app

db.create_all()

class UserTestCase(TestCase):
    """Tests for functionality related to Users."""

    def setUp(self):
        """Adds sample data and test client."""
        
        User.query.delete()

        user1 = User(
            email="test1@test1.com",
            username="testuser1",
            password="password1"
        )

        user2 = User(
            email="test2@test2.com",
            username="testuser2",
            password="password2"
        )

        db.session.add_all([user1, user2])
        db.session.commit()

        self.client = app.test_client()
        self.user1 = user1
        self.user2 = user2
    
    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
    
    def test_user_model(self):
        """Does the User model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="password"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.username, "testuser")
    
    def test_signup(self):
        "Test for signup class method."

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="password"
        )

        db.session.add(u)
        db.session.commit()

        #hashed passwords begin with $2b$
        self.assertTrue(u.password.startswith("$2b$"))
        self.assertTrue(u.username, "testuser")

    # def test_authenticate(self):
    #     """Test for authenticate class method."""

    #     test_user = User.authenticate(self.user1.username, "password1")
    #     bad_user = User.authenticate(self.user2.username, "badpassword")

    #     self.assertEqual(test_user.id, self.user1.id)
    #     self.assertFalse(bad_user)