from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50) #plaintext! issue 3
    role = models.CharField(max_length=20, default="user") #admin / user

    def __str__(self):
        return self.username


#Better way to do it:
#from django.contrib.auth.models import AbstractUser

#class User(AbstractUser):
    #role = models.CharField(max_length=20, default="user")

#Uncomment line 114 in settings.py!

#password can be set in user creation with user.set_password("1234") && user.save()
#password can be verified with user.check_password("input")
