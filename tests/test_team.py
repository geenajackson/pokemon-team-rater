"""Tests related to Team functionality."""

import os
#python debugger
import pdb
from unittest import TestCase

from models import db, User, Team

# set database to a test database before importing app

os.environ['DATABASE_URL'] = "postgresql:///teamrater-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class TeamTestCase(TestCase):
    """Tests for functionality related to Teams."""

    def setUp(self):
        """Adds sample data and test client."""
        
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

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

        team1 = Team(
            id="1111",
            name="TestTeam",
            user_id=user1.id,
            details="A test team."
        )

        db.session.add(team1)
        db.session.commit()

        team = Team.query.get(1111)


        self.user1 = user1
        self.user2 = user2
        self.team = team
    
    def tearDown(self):
        """Clean up fouled interactions."""
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_team_model(self):
        """Does the Team model work?"""

        t = Team(
            name="Test",
            user_id=self.user1.id,
            details="Testing."
        )

        db.session.add(t)
        db.session.commit()

        self.assertEqual(t.name, "Test")
    
    def test_new_team(self):
        """Test for the new team view function."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = c.post("/teams/new", data={"name": "New Team", "details": "Testing this team."})

            # Check for redirect
            self.assertEqual(resp.status_code, 302)

            team = Team.query.filter_by(name="New Team").first()
            self.assertEqual(team.details, "Testing this team.")

    def test_pokemon(self):
        """Test for adding/removing a Pokemon to a team."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = c.post("/teams/1111/add", data={"pokemon": "pikachu"})

            team = Team.query.get(1111)
            

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(team.members[0].name, "pikachu")

            resp = c.post("/teams/1111/remove", data={"pokemon": "0"})

            team = Team.query.get(1111)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(team.members, [])

    def test_edit_team(self):
        """Test for editing a specific team."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

            resp = c.post("/teams/1111/edit", data={"name": "New Name", "details": "New details."})

            team = Team.query.get(1111)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(team.name, "New Name")
            self.assertEqual(team.details, "New details.")
    
    def test_delete_team(self):
        """Test for deleting a specific team."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            
            resp = c.post("/teams/1111/delete")

            self.assertEqual(resp.status_code, 302)

            team = Team.query.get(1111)
            
            self.assertIsNone(team)