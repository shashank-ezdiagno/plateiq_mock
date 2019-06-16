from rest_framework import permissions, viewsets, status
from ..models import Invoice, InvoiceItem, VendorItem
from django.http import HttpResponseForbidden,Http404
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
        invoice = Invoice.objects.safe_get(id=id)
        if not invoice:
            raise Http404("Invoice does not exist")
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
                new_data = invoice_items_data.pop(item_id)
                item_serializer = InvoiceItemSerializer(invoice_item, data=new_data, partial=True)
                invoice_item_response[item_id] = dict(success=False)
                if item_serializer.is_valid():
                    fields = item_serializer.save()
                    invoice_item_response[item_id] = dict(success=True,fields=fields)
        items_add = data.get("items_add",[])
        invoice_item_add_response = []
        for item in items_add:
            response_add = dict(success=False)
            # check if vendor item already present
            vendor_item_dict = item.pop('item')
            vendor_item = VendorItem.objects.safe_get(vendor=invoice.vendor, item_id=vendor_item_dict["item_id"])
            if not vendor_item:
                vendor_item = VendorItem(vendor=invoice.vendor, **vendor_item_dict)
                vendor_item.last_unit_price = item["unit_price"]
                try:
                    vendor_item.save()
                except Exception as e:
                    response_add["success_vendor_item"] = False
                    invoice_item_add_response.append(response_add)
                    print(e)
                    continue

            response_add["success_vendor_item"] = True
            print(item)
            invoice_item = InvoiceItem(item=vendor_item, **item)
            invoice_item.invoice = invoice
            try:
                invoice_item.save()
            except:
                response_add["success_invoice_item"] = False
                invoice_item_add_response.append(response_add)
                continue
            response_add["success_invoice_item"] = True
            response_add["success"]=True
            invoice_item_add_response.append(response_add)


        response["items"] = invoice_item_response
        response["items_add"] = invoice_item_add_response
        return Response(response)

    def retrieve(self,request, id=None):
        invoice = Invoice.objects.get(id=id)
        invoice_items = invoice.invoiceitem_set.all()
        serializer = self.serializer_class(invoice)
        item_serializer = InvoiceItemSerializer(invoice_items,many=True)
        response = dict(invoice=serializer.data, items=item_serializer.data)
        return Response(response)




