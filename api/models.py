from django.db import models
from django.contrib.auth.models import User as Admin
from django.core.validators import RegexValidator


class Category(models.Model):
    text = models.CharField(max_length=150)
    admin = models.ForeignKey(to=Admin, on_delete=models.CASCADE)


class Question(models.Model):
    CHOICES = (("Yes", "Yes"), ("No", "No"))
    admin = models.ForeignKey(to=Admin, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category)
    text = models.CharField(max_length=300)
    status = models.BooleanField(choices=CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    fullname = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r"^\+\d{8,15}$",
        message="""
            Phone number must be entered in the format: '+9981234567'. 
            Up to 15 digits allowed.
        """,
    )

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17
    )  # Adjust max_length as needed


class Feedback(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    description = models.TextField(max_length=400)
