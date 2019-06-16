from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from ..helpers.data_management.pdf_manager import PDFHandler
from ..models import File
import datetime
import uuid

mock_buyer_id = "79365450-1fca-4fba-a2af-ef15d4bc606e"
def upload(request):
    buyer_id = mock_buyer_id
    if request.method == 'POST' and request.FILES['myfile']:
        file = request.FILES['myfile']
        handler = PDFHandler(buyer_id)
        timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
        file_name = file.name + str(timestamp)
        s3_object_id = handler.save(file_name, file.read())
        file = File.objects.create(file_name, file.size, uuid.UUID(buyer_id))
        print(file.id, file_name)


        #fs = FileSystemStorage()
        #filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        return render(request, 'upload_invoice.html', {
            'uploaded_file_id': str(file.id), 'buyer_id': buyer_id, 'buyer_name': 'Trishna'
        })
    return render(request, 'upload_invoice.html', {'buyer_id': buyer_id, 'buyer_name': 'Trishna'})