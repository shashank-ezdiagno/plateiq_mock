from django.db import models
import uuid
class InvoiceItem(models.Model):
    class Meta:
        app_label = 'invoice'
        ordering = ('invoice', 'serial_no')
        unique_together = ('invoice', 'serial_no',)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey("VendorItem", on_delete = models.PROTECT)
    quantity = models.FloatField()
    total_cost = models.FloatField()
    unit_price = models.FloatField()
    serial_no = models.IntegerField()
    invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE) # many-to-one relation
