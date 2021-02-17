from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class movies(models.Model):
    movie_title= models.CharField(max_length=200)
    genre= models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + '-'+ self.movie_title

class ratings(models.Model):
    movie_id= models.ForeignKey(movies,on_delete= models.CASCADE)
    user_id= models.IntegerField
    rating= models.IntegerField

    def __str__(self):
        return str(self.movie_id) + '-'+'-'+self.user_id + '-'+ self.rating