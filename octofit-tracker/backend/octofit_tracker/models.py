from djongo import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    members = models.JSONField()
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    points = models.IntegerField()
    def __str__(self):
        return f"{self.user}: {self.points}"
