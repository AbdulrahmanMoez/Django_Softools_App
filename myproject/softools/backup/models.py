from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True, default=None)
    pic = models.ImageField(upload_to='profile_pics', null=True, blank=True )
    gender = models.CharField(max_length=10, default='Unknown' , null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        # This is important to fix the app label issue
        app_label = 'softools'

class Service(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, null=False )
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='service_images', null=True, blank=True, default='default.png')
    url = models.CharField(max_length=200, null=True, blank=True, default='#')
    github_url = models.URLField(max_length=500, null=True, blank=True, default='#')
    available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name



class Alphabet(models.Model):
    character = models.TextField()
    
    def __str__(self):
        return self.character
    
    class Meta:
        db_table = 'Alphabet'

class Word(models.Model):
    word = models.TextField()
    type = models.TextField()
    description = models.TextField()
    id_alphabet = models.ForeignKey(
        Alphabet,
        on_delete=models.CASCADE,
        db_column='ID_ALPHABET'
    ) 
    
    
    def __str__(self):
        return self.word
    
    class Meta:
        db_table = 'Word'
    
