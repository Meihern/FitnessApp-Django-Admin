from django.contrib import admin
from Fitness.models import Client, TrainingProgram, Nutrition, ClientBaseNutrition, ClientNutritionPreference, \
    TrainingExercise, ClientTrainingDayProgram

# Register your models here.
admin.site.site_header = 'KN Fitness App'
admin.site.site_title = 'KN Fitness App'
admin.site.index_title = 'KN Fitness App'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe', 'full_age', 'full_poids', 'full_taille', 'taux_activite')
    list_filter = ('sexe',)


# @admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('client', 'nom_exercice', 'nombre_sets', 'nombre_reps', 'training_day', 'training_type')


@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ('client', 'nom_repas', 'qte_calories', 'qte_fat', 'qte_carbs', 'qte_protein', 'num_repas')


@admin.register(ClientBaseNutrition)
class ClientBaseNutritionAdmin(admin.ModelAdmin):
    list_display = ('client', 'full_kcalories', 'full_fat', 'full_carbs', 'full_proteins')


@admin.register(ClientNutritionPreference)
class ClientNutritionPreferenceAdmin(admin.ModelAdmin):
    list_display = ('client', 'full_extra_calories', 'full_fat', 'full_carbs', 'full_proteins')


@admin.register(TrainingExercise)
class TrainingExerciseAdmin(admin.ModelAdmin):
    list_display = ('nom_exercise', 'nombre_sets', 'nombre_reps')


class ExercisesInLine(admin.TabularInline):
    model = TrainingExercise


@admin.register(ClientTrainingDayProgram)
class ClientTrainingDayProgramAdmin(admin.ModelAdmin):
    list_display = ('client', 'training_type', 'training_day')
    filter_horizontal = ('exercises', )

