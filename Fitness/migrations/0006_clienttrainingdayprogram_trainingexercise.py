# Generated by Django 3.1 on 2020-08-30 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Fitness', '0005_nutrition_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_exercise', models.CharField(blank=True, db_column='exercice', max_length=50, null=True, verbose_name="Nom d'Exercice")),
                ('nombre_sets', models.PositiveSmallIntegerField(blank=True, db_column='sets', null=True, verbose_name='Nombre des Sets')),
                ('nombre_reps', models.PositiveSmallIntegerField(blank=True, db_column='reps', null=True, verbose_name='Nombre de Reps')),
            ],
            options={
                'verbose_name_plural': "Exercices d'entraînements",
                'db_table': 'Training Exercise',
            },
        ),
        migrations.CreateModel(
            name='ClientTrainingDayProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_day', models.PositiveSmallIntegerField(blank=True, db_column='train_day', null=True, verbose_name="Journée d'entraînement")),
                ('training_type', models.CharField(blank=True, db_column='type_train', max_length=255, null=True, verbose_name="Type d'entraînement")),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Fitness.client')),
                ('exercises', models.ManyToManyField(to='Fitness.TrainingExercise')),
            ],
            options={
                'verbose_name': "Journée d'entraînement Client",
                'verbose_name_plural': "Journées d'entraînement des Clients",
                'db_table': 'client_training_day',
            },
        ),
    ]
