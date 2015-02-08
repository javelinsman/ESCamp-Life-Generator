from django.db import models

# Create your models here.
class EventNode(models.Model):
    requirement = models.TextField()
    high = models.TextField()
    mid = models.TextField()
    low = models.TextField()

class EvalNode(models.Model):
    target = models.TextField()

class Story(models.Model):
    node_id = models.IntegerField()
    is_event = models.BooleanField(default=True)

class Transition(models.Model):
    content = models.TextField()
    aspect = models.CharField(max_length=10)
    is_buff = models.BooleanField(default=True)
    initial = models.IntegerField()

class TransiDecorator(models.Model):
    content = models.TextField()
    is_buff = models.BooleanField(default=True)
