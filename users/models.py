from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import RegexValidator


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_validator = RegexValidator(regex=r'^\+?1?+\d{9,15}$',
    message='El número debe tener entre 9 y quince dígitos, y puede empezar opcionalmente con un signo "+"')
    phone_number = models.CharField(blank=True, validators=[phone_validator], max_length=15)
    address = models.CharField(blank=True, max_length=80)


class Comment(models.Model):
    content = models.TextField(max_length=280)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='target')
    date = models.DateField(auto_now_add=True)


class Email(models.Model):
    email_validator = RegexValidator(regex=r'^[a-z0-9._!{}$]+@[a-z].[a-z.]',
    message='Not a valid email')
    email = models.CharField(blank=True, validators=[email_validator], max_length=254)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
