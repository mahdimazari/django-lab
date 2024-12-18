from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone


# class User(AbstractUser):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


#     def profile(self):
#         profile = Profile.objects.get(user=self)

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=1000)
#     bio = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="user_images", default="default.jpg")
#     verified = models.BooleanField(default=False)


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    file = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', related_name='notes')

    def __str__(self):
        return self.title[:30]
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # notes = models.ManyToManyField(Note, related_name="categories")  

    def __str__(self):
        return self.name
    

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Region(models.TextChoices):
    guadeloupe = "01", "01 - Guadeloupe"
    martinique = "02", "02 - Martinique"
    guyane = "03", "03 - Guyane"
    la_reunion = "04", "04 - La Réunion"
    mayotte = "06", "06 - Mayotte"
    ile_de_france = "11", "11 - Île-de-France"
    centre_val_de_loire = "24", "24 - Centre-Val de Loire"
    bourgogne_franche_comte = "27", "27 - Bourgogne-Franche-Comté"
    normandie = "28", "28 - Normandie"
    hauts_de_france = "32", "32 - Hauts-de-France"
    grand_est = "44", "44 - Grand Est"
    pays_de_la_loire = "52", "52 - Pays de la Loire"
    bretagne = "53", "53 - Bretagne"
    nouvelle_aquitaine = "75", "75 - Nouvelle-Aquitaine"
    occitanie = "76", "76 - Occitanie"
    auvergne_rhone_alpes = "84", "84 - Auvergne-Rhône-Alpes"
    provence_alpes_cote_d_azur = "93", "93 - Provence-Alpes-Côte d'Azur"
    corse = "94", "94 - Corse"

class Canteen(models.Model):
    name = models.CharField(max_length=200)
    region = models.TextField(null=True, blank=True, choices=Region.choices, verbose_name="région")
    city = models.TextField(null=True, blank=True, verbose_name="ville")
    postal_code = models.CharField(max_length=20, null=True, blank=True, verbose_name="code postal")
    daily_meal_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="repas par jour")
    admins = models.ManyToManyField(User, related_name="canteens")  # Les utilisateurs qui administrent la cantine
    consumers = models.ManyToManyField(User, related_name="consumer_canteens", verbose_name="Consommateurs")

    def __str__(self):
        return self.name



class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
    ]
    survey = models.ForeignKey(Survey, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=50)
    required = models.BooleanField(default=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, related_name="responses", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cantine = models.ForeignKey(Canteen, related_name="survey_responses", on_delete=models.CASCADE, null=True, blank=True)

class Answer(models.Model):
    response = models.ForeignKey(SurveyResponse, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    choice = models.ForeignKey(Choice, blank=True, null=True, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)




class SurveyCanteen(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="survey_canteens")
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, related_name="survey_canteens")

    def __str__(self):
        return f"{self.survey.title} - {self.canteen.name}"