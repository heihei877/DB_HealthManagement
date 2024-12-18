# Generated by Django 5.1.4 on 2024-12-18 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseRecord',
            fields=[
                ('ExerciseId', models.AutoField(primary_key=True, serialize=False)),
                ('UserId', models.IntegerField()),
                ('Type', models.CharField(max_length=30)),
                ('StartTime', models.TimeField()),
                ('EndTime', models.TimeField()),
                ('CalorieCost', models.IntegerField()),
            ],
        ),
    ]
