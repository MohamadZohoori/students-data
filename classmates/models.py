from django.db import models

class Classmates(models.Model):
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 255, default='+1-1111')
    email = models.CharField(max_length = 255, default='sth@gmail.com')
