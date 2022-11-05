from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class Curator(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


class Student(models.Model):
    name = models.CharField('ФИО', max_length=100)
    gender = models.CharField(
        'Пол',
        max_length=10,
        choices=[('male', 'Мужской'), ('female', 'Женский')],
    )
    group = models.ForeignKey(
        'Group',
        verbose_name='Группа',
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.group.students.count() < settings.MAX_GROUP_SIZE:
            return super().save(*args, **kwargs)
        raise ValidationError(
            'There should be no more than 20 people in the group',
        )

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField('Наименование группы', max_length=100)
    course = models.ForeignKey(
        'Course',
        verbose_name='Направление',
        related_name='groups',
        on_delete=models.PROTECT,

    )

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField('Наименование направления', max_length=100)
    subjects = models.ManyToManyField('Subject', verbose_name='Дисциплины')
    curator = models.ForeignKey(
        Curator,
        verbose_name='Куратор',
        related_name='courses',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField('Наименование дисциплины', max_length=100)

    def __str__(self):
        return self.name
