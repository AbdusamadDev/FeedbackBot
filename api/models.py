from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser
from django.db import models


uzbekistan_regions = [
    ("Andijon", "Andijon"),
    ("Buxoro", "Buxoro"),
    ("Farg'ona", "Farg'ona"),
    ("Jizzax", "Jizzax"),
    ("Xorazm", "Xorazm"),
    ("Namangan", "Namangan"),
    ("Navoiy", "Navoiy"),
    ("Qashqadaryo", "Qashqadaryo"),
    ("Samarqand", "Samarqand"),
    ("Sirdaryo", "Sirdaryo"),
    ("Surxandaryo", "Surxandaryo"),
    ("Toshkent", "Toshkent"),
    ("Toshkent shahar", "Toshkent shahar"),
    ("Qoraqalpog'iston", "Qoraqalpog'iston"),
]


class CustomAdmin(AbstractUser):
    telegram_id = models.IntegerField(null=True, unique=True)
    region = models.CharField(
        max_length=200, choices=uzbekistan_regions, default="Belgilanmagan"
    )


class Category(models.Model):
    title = models.CharField(max_length=150)
    admin = models.ForeignKey(to=CustomAdmin, on_delete=models.CASCADE)  # Super Admin
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Yo'nalishlar "
        verbose_name = "yo'nalish "


class User(models.Model):
    fullname = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r"^\+\d{8,15}$",
        message="""
            Telefon raqam quyidagi formatda kiritish kerak: '+9981234567'. 
            15 ta raqamgacha ruxsat berilgan.
        """,
    )

    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    region = models.CharField(max_length=50)
    subregion = models.CharField(max_length=150, default="asdasd")
    telegram_id = models.IntegerField(default=0)
    telegram_username = models.CharField(max_length=60, default="asda")

    def __str__(self) -> str:
        return f"Xodim: {self.fullname} Telefon raqam: {self.phone_number}"

    class Meta:
        verbose_name_plural = "Xodimlar "
        verbose_name = "xodim "


class Question(models.Model):
    CHOICES = ((True, "Yes"), (False, "No"))
    text = models.CharField(max_length=300)
    status = models.BooleanField(choices=CHOICES, default=False)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def is_answered(self):
        return self.status == "Yes"

    def __str__(self) -> str:
        return f"{self.text} | Javob berilgan: {self.status}"

    is_answered.boolean = True
    is_answered.short_description = "Answered?"

    class Meta:
        verbose_name_plural = "Savollar "
        verbose_name = "savol "


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=700)
    admin = models.ForeignKey(to=CustomAdmin, on_delete=models.CASCADE)  # Super Admin

    def __str__(self) -> str:
        return f"{self.question}\n\n{self.answer}"

    class Meta:
        verbose_name_plural = "Ko'p beriladigan savollar "
        verbose_name = "faq "


class Answer(models.Model):
    text = models.TextField(max_length=250)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    admin = models.ForeignKey(to=CustomAdmin, on_delete=models.CASCADE)  # Causal Admin

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name_plural = "Javoblar "
        verbose_name = "Javob "


class Regions(models.Model):
    name = models.CharField(max_length=120)
    admin = models.ForeignKey(to=CustomAdmin, on_delete=models.CASCADE)

    def __str__(self):
        return f"Hudud: {self.name} Admin: {self.admin}"

    class Meta:
        verbose_name_plural = "Hududlar "
        verbose_name = "hudud "
