from django.db import models


class Scores(models.Model):

    teams = models.CharField(max_length=120)
    url = models.TextField()
    scores = models.TextField()

    def __str__(self):
        return self.title, self.url, self.scores
