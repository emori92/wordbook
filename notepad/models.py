from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    mail_address = models.EmailField(max_length=64)
    password = models.CharField(max_length=32)
    
class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=16)
    describe = models.CharField(max_length=128, null=True)
    public = models.BooleanField()
    
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=8)
    note_id = models.IntegerField()
    
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    note_id = models.IntegerField()
    query = models.CharField(max_length=256)
    hint = models.CharField(max_length=64, null=True)
    answer = models.CharField(max_length=256)
    review = models.BooleanField()

class Star(models.Model):
    star_id = models.AutoField(primary_key=True)
    note_id = models.IntegerField()
    star_user = models.IntegerField()

class Follower(models.Model):
    follower_id = models.AutoField(primary_key=True)
    following = models.IntegerField()
    followed = models.IntegerField()
