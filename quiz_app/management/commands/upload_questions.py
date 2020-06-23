from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
import csv
from quiz_app.models import *
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('/home/appdevelopement/PycharmProjects/quize_competition/quiz_competition/media/quiz_questions.csv',
                  'rt') as file:
            reader = csv.DictReader(file, delimiter=',')
            for item in reader:
                f = Questions(question=item['question'], A=item['A'], B=item['B'], C=item['C'], D=item['D'],
                              answer=item['answer'], explanation=item['explanation'])
                print(f)
                f.save()
