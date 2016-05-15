from django.db import models
from django.db.models import CharField, PositiveSmallIntegerField, TextField


class Tvseries(models.Model):
    name = CharField(max_length=50)
    season = PositiveSmallIntegerField()
    description = TextField()
