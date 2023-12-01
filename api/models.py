from django.db import models


class Admin(models.Model):
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    # image = models.ImageField()
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Admin: {self.username}"
