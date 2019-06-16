from django.shortcuts import render
from django.conf import settings
from ..models import Invoice, InvoiceItem
from ..helpers.serializers.invoice_item_serializer import InvoiceItemSerializer
from ..helpers.serializers.invoice_serializer import InvoiceSerializer



def show(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    invoice_items = InvoiceItemSerializer(invoice.invoiceitem_set.all(),many=True)
    data = InvoiceSerializer(invoice).data
    fields = ["payment_mode","sub_total",'tax',\
                        'total','paid','refund','due','state']
    result = {}
    for field in fields:
        result[field] = data[field]


    print(invoice_items.data)
    return render(request, 'invoice.html', {
            'invoice_number': data['invoice_number'],
            'created_date': data['created_date'],
            'invoice': result,
            'vendor':data['vendor'],
            'buyer':data['buyer'],
            'items': invoice_items.data,

        })