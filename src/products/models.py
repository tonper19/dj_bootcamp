from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=220)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    inventory = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)

    def has_inventory(self):
        return self.inventory > 0

    def decrease_inventory(self, count=1, save=True):
        current_inv = self.inventory
        current_inv -= count
        self.inventory = current_inv
        if save:
            self.save()
        return self.inventory
