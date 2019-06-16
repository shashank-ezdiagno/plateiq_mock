from rest_framework import serializers
from invoice.models import VendorItem, Vendor



class VendorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorItem
        exclude = ['last_unit_price', 'vendor']

    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)

