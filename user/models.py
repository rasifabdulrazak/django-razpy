from django.db import models
from datetime import date,datetime,timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError


# Create your models here.

YEAR_CHOICES = [(y, y) for y in range(1968, date.today().year + 6)]
MONTH_CHOICE = [(m, m) for m in range(1, 13)]

def validate_year(value):
    current_year = timezone.now().year
    if value < 1968 or value > current_year + 6:
        raise ValidationError("Invalid year. Must be between 1968 and {}.".format(current_year + 6))

def validate_month(value):
    if value < 1 or value > 12:
        raise ValidationError("Invalid month. Must be between 1 and 12.")


class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    date_month = models.IntegerField(choices=MONTH_CHOICE,null=True,blank=True)
    date_year = models.IntegerField(choices=YEAR_CHOICES,null=True,blank=True)
    interval = models.CharField(max_length=55,null=True, blank=True)
    new = models.CharField(max_length=55,null=True, blank=True)
    new_int = models.DurationField(null=True,blank=True)
    new_interv = models.DurationField(null=True,blank=True)

    def __str__(self):
        return self.order_product
    
    def save(self,*args,**kwargs):
        self.interval = (datetime.now() + timedelta(days=2)) - datetime.now()
        super().save(*args, **kwargs)
    

class TestModL(models.Model):
    name = models.CharField(max_length=80,null=True,blank=True)
    is_active = models.BooleanField(default=True)

    