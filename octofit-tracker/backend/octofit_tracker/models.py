from django.db import models
from django.contrib.auth.models import AbstractUser

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

class Activity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    duration = models.IntegerField()
    calories = models.IntegerField()
    def __str__(self):
        return f"{self.user.username} - {self.type}"

class Workout(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return f"{self.user.username} - {self.name}"

class Leaderboard(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.IntegerField()
    def __str__(self):
        return f"{self.user.username} - {self.score}"