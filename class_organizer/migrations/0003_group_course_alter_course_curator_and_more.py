# Generated by Django 4.1.3 on 2022-11-01 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('class_organizer', '0002_subject_student_gender_group_course_student_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='class_organizer.course', verbose_name='Направление'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='curator',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='class_organizer.curator', verbose_name='Куратор'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='class_organizer.group', verbose_name='Группа'),
        ),
    ]
