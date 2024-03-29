from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Client(models.Model):
    SEXE_CHOICES = (('M', 'Masculin'), ('F', 'Féminin'))
    ACTIVITE_CHOICES = (('inactif', 'Inactif'), ('actif', 'Actif'), ('tres_actif', 'Très Actif'))
    nom = models.CharField(max_length=25, db_column="nom", null=False, blank=False)
    prenom = models.CharField(max_length=25, db_column="prénom", null=False, blank=False)
    sexe = models.CharField(max_length=1, db_column="sexe", null=False, blank=False, choices=SEXE_CHOICES)
    age = models.PositiveSmallIntegerField(db_column="age", null=False, blank=False)
    poids = models.DecimalField(max_digits=5, decimal_places=2, db_column="poids", blank=False, null=False,
                                validators=[MinValueValidator(Decimal('0.01'))])
    taille = models.DecimalField(max_digits=3, decimal_places=2, db_column="taille", blank=False, null=False,
                                 validators=[MinValueValidator(Decimal('0.01'))])
    taux_activite = models.CharField(max_length=15, db_column='Taux Activité', null=False, blank=False,
                                     choices=ACTIVITE_CHOICES)

    def __str__(self):
        return self.prenom + " " + self.nom

    def age_property(self):
        return '%s ans' % (str(self.age))

    def poids_property(self):
        return '%s kg' % (str(self.poids))

    def taille_property(self):
        return '%s m' % (str(self.taille))

    age_property.short_description = 'Âge'
    age_property.admin_order_field = 'age'

    full_age = property(age_property)

    poids_property.short_description = 'Poids en kg'
    poids_property.admin_order_field = 'poids'

    full_poids = property(poids_property)

    taille_property.short_description = 'Taille en m'
    taille_property.admin_order_field = 'taille'

    full_taille = property(taille_property)

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)
        if ClientBaseNutrition.objects.filter(client__pk=self.pk).exists():
            ClientBaseNutrition.objects.get(client__pk=self.pk).save()

    class Meta:
        db_table = "clients"
        verbose_name_plural = "clients"


class ClientNutritionPreference(models.Model):
    client = models.OneToOneField('Client', on_delete=models.CASCADE, unique=True)
    extra_calories = models.IntegerField(blank=False, null=False, db_column="extra_calories",
                                         verbose_name="Calories Extra")
    percentage_fat = models.DecimalField(blank=False, null=False, db_column="percentage_fat",
                                         verbose_name="Fat Percentage", max_digits=3, decimal_places=2,
                                         validators=[MinValueValidator(0)])
    percentage_carbs = models.DecimalField(blank=False, null=False, db_column="percentage_carbs",
                                           verbose_name="Carbs Percentage", max_digits=3, decimal_places=2,
                                           validators=[MinValueValidator(0)])
    percentage_proteins = models.DecimalField(blank=False, null=False, db_column="percentage_proteins",
                                              verbose_name="Proteins Percentage", max_digits=3, decimal_places=2,
                                              validators=[MinValueValidator(0)])

    def extra_calories_property(self):
        return '%s kcal' % (str(round(self.extra_calories)))

    def fat_property(self):
        return str(round(self.percentage_fat * 100)) + '%'

    def carbs_property(self):
        return str(round(self.percentage_carbs * 100)) + '%'

    def proteins_property(self):
        return str(round(self.percentage_proteins * 100)) + '%'

    extra_calories_property.short_description = 'Calories en kcal'
    extra_calories_property.admin_order_field = 'extra_calories'

    full_extra_calories = property(extra_calories_property)

    fat_property.short_description = '% de Fat'
    fat_property.admin_order_field = 'taux_fat'

    full_fat = property(fat_property)

    carbs_property.short_description = '% de Carbs'
    carbs_property.admin_order_field = 'taux_carbs'

    full_carbs = property(carbs_property)

    proteins_property.short_description = '% de Protéines'
    proteins_property.admin_order_field = 'taux_proteins'

    full_proteins = property(proteins_property)

    def __str__(self):
        return "Preferences of %s" % self.client

    def save(self, *args, **kwargs):
        super(ClientNutritionPreference, self).save(*args, **kwargs)
        if ClientBaseNutrition.objects.filter(client__pk=self.client.pk).exists():
            ClientBaseNutrition.objects.get(client__pk=self.client.pk).save()
        else:
            clientBaseNutrition = ClientBaseNutrition(client=self.client, client_nutrition_preference=self)
            clientBaseNutrition.save()

    class Meta:
        db_table = "client_nutrition_preference"
        verbose_name = "Client's Nutrition Preference"
        verbose_name_plural = "Clients Nutrition Preferences"


class ClientBaseNutrition(models.Model):
    client = models.OneToOneField('Client', on_delete=models.CASCADE, unique=True)
    client_nutrition_preference = models.OneToOneField('ClientNutritionPreference', on_delete=models.CASCADE)
    taux_kcalories = models.FloatField(blank=False, null=False, db_column="kcalories", verbose_name="Calories",
                                       validators=[MinValueValidator(0)])
    taux_fat = models.FloatField(blank=False, null=False, db_column="Fat", verbose_name="Fat",
                                 validators=[MinValueValidator(0)])
    taux_carbs = models.FloatField(blank=False, null=False, db_column="Carbs", verbose_name="Carbs",
                                   validators=[MinValueValidator(0)])
    taux_proteins = models.FloatField(blank=False, null=False, db_column="Proteins", verbose_name="Proteins",
                                      validators=[MinValueValidator(0)])

    def kcalories_property(self):
        return '%s kcal' % (str(round(self.taux_kcalories)))

    def fat_property(self):
        return '%s g' % (str(round(self.taux_fat)))

    def carbs_property(self):
        return '%s g' % (str(round(self.taux_carbs)))

    def proteins_property(self):
        return '%s g' % (str(round(self.taux_proteins)))

    kcalories_property.short_description = 'Calories en kcal'
    kcalories_property.admin_order_field = 'taux_kcalories'

    full_kcalories = property(kcalories_property)

    fat_property.short_description = 'Fat en g'
    fat_property.admin_order_field = 'taux_fat'

    full_fat = property(fat_property)

    carbs_property.short_description = 'Carbs en g'
    carbs_property.admin_order_field = 'taux_carbs'

    full_carbs = property(carbs_property)

    proteins_property.short_description = 'Proteins en g'
    proteins_property.admin_order_field = 'taux_proteins'

    full_proteins = property(proteins_property)

    def __str__(self):
        return "Calories et Macros de %s" % self.client

    def __calcul_kcalories(self):
        if self.client.sexe == 'M':
            self.taux_kcalories = (13.707 * float(self.client.poids)) + (492.3 * float(self.client.taille)) - (
                    6.673 * self.client.age) + 77.607
        elif self.client.sexe == 'F':
            self.taux_kcalories = (9.740 * float(self.client.poids)) + (172.9 * float(self.client.taille)) - (
                    4.737 * self.client.age) + 667.051

        if self.client.taux_activite == 'inactif':
            self.taux_kcalories *= 1.37

        if self.client.taux_activite == 'actif':
            self.taux_kcalories *= 1.55

        if self.client.taux_activite == 'tres_actif':
            self.taux_kcalories *= 1.8

        self.taux_kcalories += self.client_nutrition_preference.extra_calories

    def save(self, *args, **kwargs):
        self.__calcul_kcalories()
        self.taux_fat = (self.taux_kcalories / 9) * float(self.client_nutrition_preference.percentage_fat)
        self.taux_carbs = (self.taux_kcalories / 4) * float(self.client_nutrition_preference.percentage_carbs)
        self.taux_proteins = (self.taux_kcalories / 4) * float(self.client_nutrition_preference.percentage_proteins)
        super(ClientBaseNutrition, self).save(*args, **kwargs)

    class Meta:
        db_table = "calories_cacros_client"
        verbose_name = "Calories et Macros du Client"
        verbose_name_plural = "Calories et Macros des Clients"


class TrainingProgram(models.Model):
    nom_exercice = models.CharField(max_length=50, db_column="exercice", null=True, blank=True,
                                    verbose_name="Nom d'Exercice")
    nombre_sets = models.PositiveSmallIntegerField(db_column="sets", null=True, blank=True,
                                                   verbose_name="Nombre des Sets")
    nombre_reps = models.CharField(db_column="reps", null=True, blank=True, max_length=50, verbose_name="Nombre de Reps")
    training_day = models.PositiveSmallIntegerField(db_column="train_day", null=True, blank=True,
                                                    verbose_name="Journée d'entraînement")
    training_type = models.CharField(max_length=255, null=True, blank=True, db_column="type_train",
                                     verbose_name="Type d'entraînement")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nom_exercice

    class Meta:
        db_table = "Training program"
        verbose_name_plural = "Training programs"


class TrainingExercise(models.Model):
    nom_exercise = models.CharField(max_length=50, db_column="exercice", null=True, blank=True,
                                    verbose_name="Nom d'Exercice")
    nombre_sets = models.PositiveSmallIntegerField(db_column="sets", null=True, blank=True,
                                                   verbose_name="Nombre des Sets")
    nombre_reps = models.CharField(db_column="reps", max_length=50, null=True, blank=True,
                                                   verbose_name="Nombre de Reps")

    def __str__(self):
        return self.nom_exercise

    class Meta:
        db_table = "Training Exercise"
        verbose_name = "Exercice d'entraînement"
        verbose_name_plural = "Exercices d'entraînements"


class ClientTrainingDayProgram(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    training_day = models.PositiveSmallIntegerField(db_column="train_day", null=True, blank=True,
                                                    verbose_name="Journée d'entraînement")
    training_type = models.CharField(max_length=255, null=True, blank=True, db_column="type_train",
                                     verbose_name="Type d'entraînement")
    exercises = models.ManyToManyField('TrainingExercise', blank=True)

    def __str__(self):
        return "Entraînement de %s pour %s" % (self.training_type, self.client )

    class Meta:
        db_table = "client_training_day"
        verbose_name = "Journée d'entraînement Client"
        verbose_name_plural = "Journées d'entraînement des Clients"


class Nutrition(models.Model):
    nom_repas = models.TextField(verbose_name="Repas", db_column="repas", null=True, blank=True)
    qte_calories = models.FloatField(blank=True, verbose_name="Calories", null=True, db_column='Calories',
                                     validators=[MinValueValidator(0)])
    qte_fat = models.FloatField(blank=True, verbose_name="Fat", null=True, db_column="Fat",
                                validators=[MinValueValidator(0)])
    qte_carbs = models.FloatField(blank=True, verbose_name="Carbs", null=True, db_column="Carbs",
                                  validators=[MinValueValidator(0)])
    qte_protein = models.FloatField(blank=True, verbose_name="Proteins", null=True, db_column="Protein",
                                    validators=[MinValueValidator(0)])
    num_repas = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Numéro de repas",
                                                 db_column="num_repas")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nom_repas

    class Meta:
        db_table = "Nutrition"
        verbose_name_plural = "Nutritions"
