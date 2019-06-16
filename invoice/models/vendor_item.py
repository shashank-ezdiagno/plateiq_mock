from django.db import models
import uuid
class VendorItem(models.Model):
    class Meta:
        app_label = 'invoice'
        unique_together = ('item_id', 'vendor',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    last_unit_price = models.FloatField()
    vendor = models.ForeignKey("Vendor", on_delete = models.PROTECT)
    unit_of_measure = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.name


