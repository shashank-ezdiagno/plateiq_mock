from rest_framework import permissions, viewsets, status
from ..models import File
from invoice.helpers.digitization.handler import DigitizationHandler
from rest_framework.response import Response

class FileViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = File.objects.all()

    def get_permissions(self):
        return (permissions.AllowAny(),)


    def retrieve(self, request, id=None):
        file = File.objects.get(id=id)
        handler= DigitizationHandler(file)
        response = handler.__initialize__()
        if not response["success"]:
            return Response(response)
        s3_data = file.get_pdf_bytes()
        # in prod would be done asynchronously
        invoice = handler.digitize_data(s3_data)
        invoice_id=str(invoice.id)
        return Response(dict(success=True, invoice_id=invoice_id))

