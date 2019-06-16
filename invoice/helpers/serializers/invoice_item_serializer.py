from rest_framework import serializers
from .vendor_item_serializer import VendorItemSerializer
from  invoice.models import InvoiceItem, VendorItem

class InvoiceItemListSerializer(serializers.ListSerializer):
    pass

class InvoiceItemSerializer(serializers.ModelSerializer):
    item = VendorItemSerializer()

    class Meta:
        model = InvoiceItem
        #fields = '__all__'
        list_serializer_class = InvoiceItemListSerializer
        exclude= ["invoice"]


    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)


    def update(self, instance, update_dict):
        fields = ["quantity","total_cost","unit_price","serial_no"]
        update=False
        for field in fields:
            if field in update_dict:
                setattr(instance, field, update_dict[field])
                update = True
        if update:
            instance.save()
        return instance

