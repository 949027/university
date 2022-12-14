# Generated by Django 4.1.3 on 2022-11-01 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('class_organizer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование дисциплины')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], default=1, max_length=10, verbose_name='Пол'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование группы')),
                ('subjects', models.ManyToManyField(to='class_organizer.subject', verbose_name='Дисциплины')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование направления')),
                ('curator', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='class_organizer.curator', verbose_name='Куратор')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='class_organizer.group', verbose_name='Группа'),
        ),
    ]
