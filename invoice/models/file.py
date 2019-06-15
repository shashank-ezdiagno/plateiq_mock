from django.db import models
import uuid
from enum import Enum

class FileState(Enum):
    FAILED= "Upload Failed"
    ADDED = "File Added"
    PROCESSING = "Digitization In Progress"
    DIG_FAILED = "Digitization Failed"
    DIGITIZED = "Digitized"


class File(models.Model):
    class Meta:
        app_label = 'invoice'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    s3_object_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    size_in_bytes = models.FloatField()
    created_date = models.DateTimeField(auto_now_add = True)
    state = models.CharField(
              max_length=20,
              choices=[(state, state.value) for state in FileState]  # Choices is a list of Tuple
            )


