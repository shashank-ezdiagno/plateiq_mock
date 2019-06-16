from django.test import TestCase
from invoice.helpers.data_management.pdf_manager import PDFHandler
from invoice.models import File, Buyer
import uuid
import os
import hashlib
import datetime

# Create your tests here.
class S3TestClass(TestCase):

    @classmethod
    def setUpClass(cls):
        super(S3TestClass, cls).setUpClass()
        buyer = Buyer(name="ABC Enterprises", address_full_address="abc path, abc city, abc")
        buyer.save()


    def setUp(self):
        # Setup run before every test method.
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_name = "Sample-Retail.pdf"
        self.pdf_path = os.path.join(dir_path, "mock_pdf", file_name)
        timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
        self.file_name = file_name + str(timestamp)
        self.file_hash_name = hashlib.sha1(self.file_name.encode('utf-8')).hexdigest()
        self.buyer = Buyer.objects.get()

    def tearDown(self):
        # Clean up run after every test method.
        if hasattr(self, 'file_object'):
            self.file_object.delete()
        handler = PDFHandler(str(self.buyer.id))
        handler.delete(self.file_name)

    @classmethod
    def tearDownClass(cls):
        buyer = Buyer.objects.get()
        buyer.delete()

    def test_save_s3(self):
        handler = PDFHandler(str(self.buyer.id))
        file_data = open(self.pdf_path, 'rb')
        statinfo = os.stat(self.pdf_path)
        size = statinfo.st_size
        print(size)
        file_hash_name = handler.save(self.file_name, file_data.read())
        file = File.objects.create(self.file_name, size, self.buyer.id)
        print(file.id, self.file_name)
        self.file_object = file
        self.assertEqual(file.buyer.id, self.buyer.id)
        self.assertEqual(file.name, self.file_name)
        self.assertEqual(file.size_in_bytes, size)

    def test_get_s3(self):
        handler = PDFHandler(str(self.buyer.id))
        file_data = open(self.pdf_path, 'rb')
        file_hash_name = handler.save(self.file_name, file_data.read())
        data = handler.get(self.file_name)
        file_data = open(self.pdf_path, 'rb')
        self.assertEqual(file_data.read(), data.read())
