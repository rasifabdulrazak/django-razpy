# Generated by Django 4.2.7 on 2024-08-29 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0013_alter_order_interval"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="interval",
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]
