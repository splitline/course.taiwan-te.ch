from django.db import models
from django.contrib.auth.models import User
from parser.models import Courses


class SelectedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    type = models.SmallIntegerField(default=1) # 1:SELECT / 2:FAVORITE
    