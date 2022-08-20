from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=30)
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Fileupload(models.Model):
    file = models.FileField(upload_to="media/",null=False)
    filename = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    date = models.DateField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user',verbose_name='owner')
