from rest_framework import permissions, viewsets, status
from ..models import Invoice, InvoiceItem
from ..helpers.serializers.invoice_serializer import InvoiceSerializer
from ..helpers.serializers.invoice_item_serializer import InvoiceItemSerializer
from rest_framework.response import Response

class InvoiceViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_permissions(self):
        return (permissions.AllowAny(),)


    def partial_update(self, request, id=None):
        invoice = Invoice.objects.get(id=id)
        data = request.data
        invoice_data = data["invoice"]

        serializer = self.serializer_class(invoice, data=invoice_data, partial=True)
        response = dict(success=False)
        if serializer.is_valid():
            response["success"] = True
            serializer.save()
        else:
            response["errors"] = serializer.errors
        invoice_items_data = data.get("items")
        if  invoice_items_data:
            invoice_items = InvoiceItem.objects.filter(invoice_id=id)
            for invoice_item in invoice_items:
                item_id = str(invoice_item.id)
                if item_id not in invoice_items_data:
                    continue
                new_data = invoice_items_data[item_id]
                item_serializer = InvoiceItemSerializer(invoice_item, data=new_data, partial=True)
                if item_serializer.is_valid():
                    item_serializer.save()

        return Response(response)

