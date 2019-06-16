from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Buyer, File, Invoice, InvoiceItem, Vendor, VendorItem

admin.site.register(Buyer)
admin.site.register(File)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Vendor)
admin.site.register(VendorItem)
