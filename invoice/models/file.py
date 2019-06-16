from django.db import models
import uuid
from enum import Enum
from invoice.helpers.data_management.pdf_manager import PDFHandler

class FileState(Enum):
    FAILED= "Upload Failed"
    FILE_ADDED = "File Added"
    IN_PROGRESS = "Digitization In Progress"
    DIG_FAILED = "Digitization Failed"
    PARTIAL_DIGITIZED = "Under Review"
    DIGITIZED = "Uploaded"

class FileManager(models.Manager):
    def create(self, name, size, buyer_id):
        file = self.model(name=name,
                          size_in_bytes=size,
                          buyer_id=buyer_id,
                          state=FileState.FILE_ADDED.name)
        file.save(using=self._db)
        return file

    def safe_get(self, *args, **kwargs):
        try:
            value = self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            value = None
        return value


class File(models.Model):
    class Meta:
        app_label = 'invoice'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey("Buyer", on_delete = models.PROTECT)
    name = models.CharField(max_length=100)
    size_in_bytes = models.FloatField()
    created_date = models.DateTimeField(auto_now_add = True)
    state = models.CharField(
              max_length=20,
              choices=[(state.name, state.value) for state in FileState]  # Choices is a list of Tuple
            )
    objects = FileManager()

    def get_pdf_bytes(self):
        pdf_handler = PDFHandler(str(self.buyer.id))
        s3_data = pdf_handler.get(self.name)
        return s3_data.read()


