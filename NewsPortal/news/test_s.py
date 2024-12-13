from django.db import models

class Topping(models.Model):
    pass

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)

from django.db.models.signals import m2m_changed

def topings_changed(sender, **kwargs):
    pass

m2m_changed.connect(topings_changed, sender=Pizza.toppings.through)
