from django.db import models
from datetime import datetime


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    mail_address = models.EmailField()
    password = models.CharField(max_length=32)
    created_at = models.DateTimeField(default=datetime.now())

class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=16)
    describe = models.CharField(max_length=128, null=True)
    public = models.BooleanField()
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    note_id = models.IntegerField()
    query = models.CharField(max_length=256)
    hint = models.CharField(max_length=64, null=True)
    answer = models.CharField(max_length=256)
    review = models.BooleanField()
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=8)
    note_id = models.IntegerField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

class Star(models.Model):
    star_id = models.AutoField(primary_key=True)
    note_id = models.IntegerField()
    star_user = models.IntegerField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Follower(models.Model):
    follower_id = models.AutoField(primary_key=True)
    following = models.IntegerField()
    followed = models.IntegerField()
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE)
