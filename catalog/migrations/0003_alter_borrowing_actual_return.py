# Generated by Django 5.0.6 on 2024-05-13 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="actual_return",
            field=models.DateField(blank=True),
        ),
    ]
