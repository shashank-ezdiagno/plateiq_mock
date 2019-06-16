from rest_framework import serializers

from  invoice.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name","address_full_address"]

