from django.db import models
from datetime import date
from random import choice

from .countries import COUNTRIES


def get_random_country():
    return choice(COUNTRIES)[0]

class DailySolution(models.Model):
    date = models.DateField(unique=True, default=date.today)
    solution = models.TextField(choices=COUNTRIES, default=get_random_country)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
