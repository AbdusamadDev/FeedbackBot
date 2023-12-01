from django.db import models
from django.contrib.auth.models import User as Admin
from django.core.validators import RegexValidator


class Category(models.Model):
    title = models.CharField(max_length=150)
    admin = models.ForeignKey(to=Admin, on_delete=models.CASCADE)  # Super Admin
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class User(models.Model):
    fullname = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r"^\+\d{8,15}$",
        message="""
            Phone number must be entered in the format: '+9981234567'. 
            Up to 15 digits allowed.
        """,
    )

    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    region = models.CharField(max_length=50)


class Question(models.Model):
    CHOICES = (("Yes", "Yes"), ("No", "No"))
    text = models.CharField(max_length=300)
    status = models.BooleanField(choices=CHOICES, default=False)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def is_answered(self):
        return self.status == "Yes"

    def __str__(self) -> str:
        return f"{self.text} | Javob berilgan: {self.status}"

    is_answered.boolean = True
    is_answered.short_description = "Answered?"


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=700)
    admin = models.ForeignKey(to=Admin, on_delete=models.CASCADE)  # Super Admin

    def __str__(self) -> str:
        return f"{self.question}\n\n{self.answer}"


class Answer(models.Model):
    text = models.TextField(max_length=250)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    admin = models.ForeignKey(to=Admin, on_delete=models.CASCADE)  # Causal Admin

    def __str__(self) -> str:
        return self.text
