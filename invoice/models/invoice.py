from django.db import models
import uuid
from enum import Enum

class InvoiceState(Enum):
    FILE_ADDED = "File Added"
    IN_PROGRESS = "Digitization In Progress"
    DIG_FAILED = "Digitization Failed"
    PARTIAL_DIGITIZED = "Under Review"
    DIGITIZED = "Uploaded"

class PaymentMode(Enum):
    CASH = "Cash"
    CREDIT = "Credit Card"
    DEBIT = "Debit Card"


class InvoiceManager(models.Manager):
    def create_from_pdf(self, file, buyer):
        invoice = self.model(file=file, buyer=buyer, state=InvoiceState.FILE_ADDED.name)
        invoice.save(using=self._db)
        return invoice

    def safe_get(self, *args, **kwargs):
        try:
            value = self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            value = None
        return value


class Invoice(models.Model):
    class Meta:
        app_label = 'invoice'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey("File", on_delete = models.PROTECT)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.ForeignKey("Vendor", on_delete = models.PROTECT, null=True, blank=True)
    buyer = models.ForeignKey("Buyer", on_delete = models.PROTECT, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    payment_mode = models.CharField(max_length=20,
              choices=[(mode.name, mode.value) for mode in PaymentMode], null=True, blank=True )
    sub_total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15)
    tax = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15)
    total = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15)
    paid = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15)
    refund = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15)
    due = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15)
    state = models.CharField(
              max_length=20,
              choices=[(state.name, state.value) for state in InvoiceState]  # Choices is a list of Tuple
            )
    objects = InvoiceManager()


