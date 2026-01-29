from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import models as app_models

from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        Team = self.get_or_create_team_model()
        Activity = self.get_or_create_activity_model()
        Leaderboard = self.get_or_create_leaderboard_model()
        Workout = self.get_or_create_workout_model()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User(username='ironman', email='ironman@marvel.com', team=marvel),
            User(username='captainamerica', email='cap@marvel.com', team=marvel),
            User(username='batman', email='batman@dc.com', team=dc),
            User(username='superman', email='superman@dc.com', team=dc),
        ]
        for user in users:
            user.set_password('password123')
            user.save()

        # Create activities
        activities = [
            Activity(user=users[0], type='run', duration=30, calories=300),
            Activity(user=users[1], type='cycle', duration=45, calories=400),
            Activity(user=users[2], type='swim', duration=60, calories=500),
            Activity(user=users[3], type='walk', duration=20, calories=100),
        ]
        for activity in activities:
            activity.save()

        # Create workouts
        workouts = [
            Workout(user=users[0], name='Chest Day', description='Bench press, pushups'),
            Workout(user=users[1], name='Leg Day', description='Squats, lunges'),
            Workout(user=users[2], name='Cardio', description='Running, cycling'),
            Workout(user=users[3], name='Strength', description='Deadlift, pullups'),
        ]
        for workout in workouts:
            workout.save()

        # Create leaderboard
        Leaderboard.objects.create(user=users[0], score=1000)
        Leaderboard.objects.create(user=users[1], score=900)
        Leaderboard.objects.create(user=users[2], score=1100)
        Leaderboard.objects.create(user=users[3], score=950)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

    def get_or_create_team_model(self):
        from django.db import models
        class Team(models.Model):
            name = models.CharField(max_length=100, unique=True)
            def __str__(self):
                return self.name
            class Meta:
                app_label = 'octofit_tracker'
        return Team

    def get_or_create_activity_model(self):
        from django.db import models
        User = get_user_model()
        class Activity(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            type = models.CharField(max_length=50)
            duration = models.IntegerField()
            calories = models.IntegerField()
            class Meta:
                app_label = 'octofit_tracker'
        return Activity

    def get_or_create_leaderboard_model(self):
        from django.db import models
        User = get_user_model()
        class Leaderboard(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            score = models.IntegerField()
            class Meta:
                app_label = 'octofit_tracker'
        return Leaderboard

    def get_or_create_workout_model(self):
        from django.db import models
        User = get_user_model()
        class Workout(models.Model):
            user = models.ForeignKey(User, on_delete=models.CASCADE)
            name = models.CharField(max_length=100)
            description = models.TextField()
            class Meta:
                app_label = 'octofit_tracker'
        return Workout
