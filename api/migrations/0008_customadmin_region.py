# Generated by Django 4.2.7 on 2023-12-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_remove_customadmin_region"),
    ]

    operations = [
        migrations.AddField(
            model_name="customadmin",
            name="region",
            field=models.CharField(choices=[], default="nanna", max_length=200),
        ),
    ]
