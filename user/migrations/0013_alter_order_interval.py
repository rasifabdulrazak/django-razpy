# Generated by Django 4.2.7 on 2024-08-29 09:32

from django.db import migrations, models

# Generated by Django 4.2.7 on 2024-08-29 09:31




class Migration(migrations.Migration):
    dependencies = [
        ("user", "0012_order_new_int_alter_order_new"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="interval",
            field=models.DurationField(blank=True, max_length=55, null=True),
        ),
    ]
