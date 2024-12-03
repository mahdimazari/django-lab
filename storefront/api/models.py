from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


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
    

