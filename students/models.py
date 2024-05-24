from django.db import models

class Candidate(models.Model):
    candidate = models.CharField(max_length=100)
    score = models.IntegerField()
    scoring_date = models.DateField()
    province = models.CharField(max_length=100)

