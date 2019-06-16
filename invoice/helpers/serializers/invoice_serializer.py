from rest_framework import serializers
from .vendor_serializer import VendorSerializer
from .buyer_serializer import BuyerSerializer
from  invoice.models import Invoice, Vendor, Buyer, File


class InvoiceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    buyer = BuyerSerializer()
    #file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all())
    created_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Invoice
        fields = ['vendor','buyer','file','invoice_number', 'created_date', 'payment_mode', 'sub_total', 'tax', 'total', 'paid', 'refund', 'due', 'state']


    def update(self, instance, update_dict):
        fields = ["invoice_number", "created_date","payment_mode","sub_total","tax","total","paid","refund","due","state"]
        update=False
        for field in fields:
            if field in update_dict:
                if field == 'state' and update_dict[field] == 'DIGITIZED':
                    instance.file.state = update_dict[field]
                    instance.file.save()
                setattr(instance, field, update_dict[field])
                update = True
        if update:
            instance.save()
        return instance
