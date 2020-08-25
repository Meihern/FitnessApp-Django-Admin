from django.contrib import admin
from Fitness.models import Client, TrainingProgram, Nutrition, ClientBaseNutrition, ClientNutritionPreference


# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe', 'full_age', 'full_poids', 'full_taille', 'taux_activite')
    list_filter = ('sexe',)


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('nom_exercice', 'nombre_sets', 'nombre_reps')


@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ('nom_repas', 'qte_calories', 'qte_fat', 'qte_carbs', 'qte_protein')


@admin.register(ClientBaseNutrition)
class ClientBaseNutritionAdmin(admin.ModelAdmin):
    list_display = ('client', 'full_kcalories', 'full_fat', 'full_carbs', 'full_proteins')


@admin.register(ClientNutritionPreference)
class ClientNutritionPreferenceAdmin(admin.ModelAdmin):
    list_display = ('client', 'extra_calories', 'percentage_fat', 'percentage_carbs', 'percentage_proteins')
