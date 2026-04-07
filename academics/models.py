from django.db import models


class AcademicTerm(models.Model):
    name = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.year}"


class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)

    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"