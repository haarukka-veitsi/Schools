from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Person(models.Model):
    fio = models.CharField(max_length=100)
    birth_date = models.IntegerField(validators=[MinValueValidator(1920), MaxValueValidator(2025)])

    class Meta:
        abstract = True


class Employee(Person):
    pass


class School(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MinValueValidator(1400), MaxValueValidator(2024)])
    director = models.ForeignKey(Employee, on_delete=models.PROTECT)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])


class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField(validators=[MaxValueValidator(30)])
    teacher = models.ForeignKey(Employee, on_delete=models.PROTECT)


class Student(Person):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.PROTECT)