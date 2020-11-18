# Generated by Django 3.1 on 2020-10-26 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fitness', '0007_auto_20200830_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienttrainingdayprogram',
            name='exercises',
            field=models.ManyToManyField(blank=True, to='Fitness.TrainingExercise'),
        ),
        migrations.AlterField(
            model_name='trainingprogram',
            name='nombre_reps',
            field=models.CharField(blank=True, db_column='reps', max_length=50, null=True, verbose_name='Nombre de Reps'),
        ),
    ]