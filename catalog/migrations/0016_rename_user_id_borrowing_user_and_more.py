# Generated by Django 4.2.15 on 2024-08-21 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0015_alter_borrowing_book"),
    ]

    operations = [
        migrations.RenameField(
            model_name="borrowing",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="payment",
            old_name="type",
            new_name="types",
        ),
    ]
