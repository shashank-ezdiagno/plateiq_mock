from django.db import models
import uuid
from enum import Enum

class InvoiceState(Enum):
    FILE_ADDED = "File Added"
    IN_PROGRESS = "Digitization In Progress"
    PARTIAL_DIGITIZED = "Under Review"
    DIGITIZED = "Uploaded"


class Invoice(models.Model):
    class Meta:
        app_label = 'invoice'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey("File", on_delete = models.PROTECT)
    invoice_number = models.CharField(max_length=50)
    vendor = models.ForeignKey("Vendor", on_delete = models.PROTECT)
    buyer = models.ForeignKey("Buyer", on_delete = models.PROTECT)
    created_date = models.DateTimeField()
    state = models.CharField(
              max_length=20,
              choices=[(state, state.value) for state in InvoiceState]  # Choices is a list of Tuple
            )


