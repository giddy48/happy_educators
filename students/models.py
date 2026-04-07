from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    admission_no = models.CharField(max_length=20)
    class_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name