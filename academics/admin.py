from django.contrib import admin
from .models import SchoolClass, Student, Teacher, Subject, Mark

admin.site.register(SchoolClass)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Mark)