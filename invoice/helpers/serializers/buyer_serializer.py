from rest_framework import serializers

from  invoice.models import Buyer


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ["name","address_full_address"]

