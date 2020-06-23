from django.db import models
from django.contrib.auth.models import User


class Questions(models.Model):
    object = models.Manager()
    question = models.TextField(blank=True, null=True)
    A = models.CharField(max_length=128, blank=True, null=True)
    B = models.CharField(max_length=128, blank=True, null=True)
    C = models.CharField(max_length=128, blank=True, null=True)
    D = models.CharField(max_length=128, blank=True, null=True)
    answer = models.CharField(max_length=128, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        template = '{0.question} {0.A} {0.B} {0.C} {0.D} {0.answer} {0.explanation}'
        return template.format(self)


class UserAnswerDetails(models.Model):
    object = models.Manager()
    contestant = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(blank=True, null=True)
    answer = models.CharField(max_length=128, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        template = '{0.contestant} {0.question} {0.answer} {0.score} {0.time}'
        return template.format(self)
