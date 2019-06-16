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
        response = dict(success_invoice=False)
        if serializer.is_valid():
            response["success_invoice"] = True
            serializer.save()
        else:
            response["errors_invoice"] = serializer.errors
        invoice_items_data = data.get("items")
        invoice_item_response = {}
        if  invoice_items_data:
            invoice_items = invoice.invoiceitem_set.all()
            for invoice_item in invoice_items:
                item_id = str(invoice_item.id)
                if item_id not in invoice_items_data:
                    continue
                new_data = invoice_items_data[item_id]
                item_serializer = InvoiceItemSerializer(invoice_item, data=new_data, partial=True)
                invoice_item_response[item_id] = dict(success=False)
                if item_serializer.is_valid():
                    fields = item_serializer.save()
                    invoice_item_response[item_id] = dict(success=True,fields=fields)
        response["items"] = invoice_item_response

        return Response(response)

    def retrieve(self,request, id=None):
        invoice = Invoice.objects.get(id=id)
        invoice_items = invoice.invoiceitem_set.all()
        serializer = self.serializer_class(invoice)
        item_serializer = InvoiceItemSerializer(invoice_items,many=True)
        response = dict(invoice=serializer.data, items=item_serializer.data)
        return Response(response)




