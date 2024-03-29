from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import now

from Fitness.models import Client, Nutrition, ClientBaseNutrition, ClientNutritionPreference, \
    TrainingExercise, ClientTrainingDayProgram
# Register your models here.
from PDF.utils import render_to_pdf

admin.site.site_header = 'KN Fitness App'
admin.site.site_title = 'KN Fitness App'
admin.site.index_title = 'KN Fitness App'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe', 'full_age', 'full_poids', 'full_taille', 'taux_activite', 'client_actions')
    list_filter = ('sexe',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^(?P<client_id>.+)/generate_pdf/$',
                self.admin_site.admin_view(self.generate_pdf),
                name='generate-pdf'
                )]

        return custom_urls + urls

    def client_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">PDF</a>',
            reverse('admin:generate-pdf', args=[obj.pk])
        )

    client_actions.short_description = 'Générer sous format PDF'
    client_actions.allow_tags = True

    def generate_pdf(self, request, client_id, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_id)
        extra_calories = ClientNutritionPreference.objects.get(client=client).extra_calories
        if extra_calories > 0:
            objectif =  'Prise du Poids'
        elif extra_calories == 0:
            objectif = 'Stabilité du Poids'
        else:
            objectif = 'Perte du Poids'


        context = {
            'nom_prenom': client.prenom + ' ' + client.nom,
            'age': client.full_age,
            'taille': client.full_taille,
            'poids': client.full_poids,
            'calories': ClientBaseNutrition.objects.get(client=client).full_kcalories,
            'objectif': objectif,
            'repas': list(Nutrition.objects.filter(client=client).order_by('num_repas')),
            'trainings': list(ClientTrainingDayProgram.objects.filter(client=client).order_by('training_day')),
            'date': now().date(),
        }
        if context:
            template_name = 'PDF/clientPDF.html'
            template = get_template(template_name)
            html = template.render(context)
            pdf = render_to_pdf(template_name, context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Programme_%s.pdf" % (context['nom_prenom'].replace(' ', '_'))
                content = "inline; filename=%s" % filename
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename=%s" % filename
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        else:
            return HttpResponse("No context")


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
    filter_horizontal = ('exercises',)
