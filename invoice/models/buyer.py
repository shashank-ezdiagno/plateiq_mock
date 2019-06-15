from django.db import models
import uuid

class BuyerManager(models.Manager):
    pass

class Buyer(models.Model):
    class Meta:
        app_label = 'invoice'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    address_full_address = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)
    description = models.TextField(null=True)
    geo_location_lat = models.FloatField(null=True)
    geo_location_lng = models.FloatField(null=True)
    phone = models.TextField(blank=True, null=True)
    objects = BuyerManager()

    def __str__(self):
        return self.name