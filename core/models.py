# core/models.py
from django.db import models

class BaseModel(models.Model):
    # Define your BaseModel fields and methods here
    class Meta:
        abstract = True


from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
   
