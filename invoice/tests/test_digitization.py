from django.test import TestCase
from invoice.models import *
from invoice.helpers.common_utils import CommonUtils
from invoice.helpers.data_management.pdf_manager import PDFHandler
import os
import datetime

# Create your tests here.
class DigitizationTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        super(DigitizationTestClass, cls).setUpClass()
        # create buyer
        buyer = Buyer(name="ABC Enterprises", address_full_address="abc path, abc city, abc")
        buyer.save()
        # create vendr
        vendor = Vendor(name="ABC Restaurant", address_full_address="def path, def city, def")
        vendor.save()
        # create file
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_name = "Sample-Retail.pdf"
        pdf_path = os.path.join(dir_path, "mock_pdf", file_name)
        statinfo = os.stat(pdf_path)
        size = statinfo.st_size
        timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
        file_name = file_name + str(timestamp)
        handler = PDFHandler(str(buyer.id))
        file_data = open(pdf_path, 'rb')
        file_hash_name = handler.save(file_name, file_data.read())
        file = File.objects.create(file_name, size, buyer.id)

        # vendor_items
        items = [{
                    "name":"Apple",
                    "category": "Fruit",
                    "last_unit_price": CommonUtils.generate_random_int(100,1000),
                    "unit_of_measure": "Kg"
                  },
                  {
                    "name":"Banana",
                    "category": "Fruit",
                    "last_unit_price": CommonUtils.generate_random_int(30,100),
                    "unit_of_measure": "Kg"
                  },
                  {
                    "name":"Aashirvaad Atta 5Kg",
                    "category": "Flour",
                    "last_unit_price": CommonUtils.generate_random_int(100,1000),
                    "unit_of_measure": "pcs"
                  },
                  {
                    "name":"Milk Nandini 500ml",
                    "category": "Dairy",
                    "last_unit_price": CommonUtils.generate_random_int(10,100),
                    "unit_of_measure": "pcs"
                  },
                  {
                    "name":"Real Juice 1Ltr",
                    "category": "Beverage",
                    "last_unit_price": CommonUtils.generate_random_int(100,1000),
                    "unit_of_measure": "pcs"
                  }]

        for i,item in enumerate(items):
            vendor_item = VendorItem(vendor=vendor, item_id=i+100, **item)
            vendor_item.save()


    def setUp(self):
        # Setup run before every test method.
        from invoice.helpers.digitization.handler import DigitizationHandler
        self.file = File.objects.get()
        self.handler= DigitizationHandler(self.file)
        self.vendor = Vendor.objects.get()
        self.buyer = Buyer.objects.get()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_digitization_init(self):
        response = self.handler.__initialize__()
        self.assertEqual(response['success'], True)
        invoice = response["invoice"]


    def test_digitization(self):
        response = self.handler.__initialize__()
        self.assertEqual(response['success'], True)
        invoice_prev = response["invoice"]
        s3_data = self.file.get_pdf_bytes()
        invoice = self.handler.digitize_data(s3_data)
        self.assertEqual(invoice_prev.id, invoice.id)
        invoice_items = invoice.invoiceitem_set.all()
        print(invoice_items)
        for item in invoice_items:
            print(item.id)

