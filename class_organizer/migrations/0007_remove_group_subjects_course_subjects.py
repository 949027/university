# Generated by Django 4.1.3 on 2022-11-02 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_organizer', '0006_alter_course_curator_alter_group_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='subjects',
        ),
        migrations.AddField(
            model_name='course',
            name='subjects',
            field=models.ManyToManyField(to='class_organizer.subject', verbose_name='Дисциплины'),
        ),
    ]
