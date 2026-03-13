from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

from pymongo import MongoClient

User = get_user_model()

TEAM_DATA = [
    {"name": "Marvel", "members": ["Iron Man", "Captain America", "Thor", "Hulk", "Black Widow"]},
    {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman", "Flash", "Aquaman"]},
]

ACTIVITIES = [
    {"name": "Running", "unit": "km"},
    {"name": "Cycling", "unit": "km"},
    {"name": "Swimming", "unit": "laps"},
]

WORKOUTS = [
    {"name": "Morning Cardio", "description": "30 min run + 10 min HIIT"},
    {"name": "Strength Training", "description": "Upper body weights"},
]

LEADERBOARD = [
    {"user": "Iron Man", "points": 120},
    {"user": "Superman", "points": 150},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation and raw operations
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users and teams
        users = []
        for team in TEAM_DATA:
            for member in team["members"]:
                user_doc = {"name": member, "email": f"{member.lower().replace(' ', '')}@octofit.com", "team": team["name"]}
                users.append(user_doc)
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Create teams
        teams = [{"name": t["name"], "members": t["members"]} for t in TEAM_DATA]
        db.teams.insert_many(teams)

        # Create activities
        db.activities.insert_many(ACTIVITIES)

        # Create workouts
        db.workouts.insert_many(WORKOUTS)

        # Create leaderboard
        db.leaderboard.insert_many(LEADERBOARD)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
