# Generated by Django 3.1 on 2020-08-23 16:36

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(db_column='nom', max_length=25)),
                ('prenom', models.CharField(db_column='prénom', max_length=25)),
                ('sexe', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], db_column='sexe', max_length=1)),
                ('age', models.PositiveSmallIntegerField(db_column='age')),
                ('poids', models.DecimalField(db_column='poids', decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('taille', models.DecimalField(db_column='taille', decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('taux_activite', models.CharField(choices=[('inactif', 'Inactif'), ('actif', 'Actif'), ('tres_actif', 'Très Actif')], db_column='Taux Activité', max_length=15)),
            ],
            options={
                'verbose_name_plural': 'clients',
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_repas', models.CharField(db_column='repas', max_length=75, verbose_name='Repas')),
                ('qte_calories', models.FloatField(db_column='Calories', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Calories')),
                ('qte_fat', models.FloatField(db_column='Fat', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Fat')),
                ('qte_carbs', models.FloatField(db_column='Carbs', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Carbs')),
                ('qte_protein', models.FloatField(db_column='Protein', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Proteins')),
            ],
            options={
                'verbose_name_plural': 'Nutritions',
                'db_table': 'Nutrition',
            },
        ),
        migrations.CreateModel(
            name='TrainingProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_exercice', models.CharField(db_column='exercice', max_length=50)),
                ('nombre_sets', models.PositiveSmallIntegerField(db_column='sets')),
                ('nombre_reps', models.PositiveSmallIntegerField(db_column='reps')),
            ],
            options={
                'verbose_name_plural': 'Training programs',
                'db_table': 'Training program',
            },
        ),
        migrations.CreateModel(
            name='ClientNutritionPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_calories', models.PositiveIntegerField(db_column='extra_calories', verbose_name='Calories Extra')),
                ('percentage_fat', models.DecimalField(db_column='percentage_fat', decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Fat Percentage')),
                ('percentage_carbs', models.DecimalField(db_column='percentage_carbs', decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Carbs Percentage')),
                ('percentage_proteins', models.DecimalField(db_column='percentage_proteins', decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Proteins Percentage')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Fitness.client')),
            ],
            options={
                'verbose_name': "Client's Nutrition Preference",
                'verbose_name_plural': 'Clients Nutrition Preferences',
                'db_table': 'client_nutrition_preference',
            },
        ),
        migrations.CreateModel(
            name='ClientBaseNutrition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taux_kcalories', models.FloatField(db_column='kcalories', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Calories')),
                ('taux_fat', models.FloatField(db_column='Fat', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Fat')),
                ('taux_carbs', models.FloatField(db_column='Carbs', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Carbs')),
                ('taux_proteins', models.FloatField(db_column='Proteins', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Proteins')),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Fitness.client')),
                ('client_nutrition_preference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Fitness.clientnutritionpreference')),
            ],
            options={
                'verbose_name': 'Calories et Macros du Client',
                'verbose_name_plural': 'Calories et Macros des Clients',
                'db_table': 'calories_cacros_client',
            },
        ),
    ]
