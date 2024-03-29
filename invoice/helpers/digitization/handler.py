from ..data_management.pdf_manager import PDFHandler
from invoice.models import File, Vendor, Invoice, VendorItem, InvoiceItem
from invoice.models.invoice import PaymentMode, InvoiceState
from invoice.models.file import FileState
from ..common_utils import CommonUtils
import datetime


class DigitizationHandler():
    def __init__(self, file):
        self.file = file


    def __initialize__(self):
        response = dict(success=True)
        if not self.file:
            response["success"]=False
            response["message"]="File Not Found"
        elif self.file.state == FileState.IN_PROGRESS.name:
            response["success"]=False
            response["message"]="Already in Progress"
        elif self.file.state == FileState.PARTIAL_DIGITIZED.name:
            response["success"]=False
            response["message"]="Under Review"
        elif self.file.state == FileState.DIGITIZED.name:
            response["success"]=False
            response["message"]="Already Uploaded"
        if not response["success"]:
            response["invoice_id"] = str(self.file.invoice_set.get().id)
            return response
        self.invoice = Invoice.objects.create_from_pdf(self.file, self.file.buyer)
        return dict(success=True, invoice=self.invoice)

    def digitize_data(self, ptr):
        # processing invoice
        ptr, self.invoice.vendor_id= VendorHandler.extract_vendor(ptr)
        ptr, self.invoice.invoice_number = InvoiceNumberHandler.extract_invoice_number(ptr)
        ptr, self.invoice.created_date = CreationDateHandler().extract_date_bytes(ptr)
        self.invoice.payment_mode = PaymentMode.CASH.name
        ptr, invoice_items = self.get_invoice_items(ptr)
        sub_total = 0
        for item in invoice_items:
            sub_total+=item.total_cost
        self.invoice.sub_total = sub_total
        self.invoice.tax = self.invoice.sub_total/10.0
        self.invoice.total = self.invoice.sub_total * 1.1
        self.invoice.paid = self.invoice.total
        self.invoice.refund = self.invoice.paid - self.invoice.total if self.invoice.paid > self.invoice.total else 0
        self.invoice.due = self.invoice.total - self.invoice.paid if self.invoice.paid < self.invoice.total else 0
        self.invoice.state = InvoiceState.PARTIAL_DIGITIZED.name
        self.invoice.save()
        self.file.state = FileState.PARTIAL_DIGITIZED.name
        self.file.save()
        return self.invoice

    def get_invoice_items(self, ptr):
        generator = MockInvoiceItemGenerator(self.invoice)
        return ptr, generator.generate_data()





class VendorHandler():
    @staticmethod
    def get_mock_vendor_data():
        return Vendor.objects.all().first()
    @staticmethod
    def extract_vendor(file_ptr):
        # vendor data extraction logic
        vendor_data = VendorHandler.get_mock_vendor_data()
        # get  or create vendor from db
        return file_ptr, str(vendor_data.id)

class InvoiceNumberHandler():
    @staticmethod
    def extract_invoice_number(file_ptr):
        invoice_id = CommonUtils.generate_random_id()
        return file_ptr, invoice_id

class CreationDateHandler():
    def extract_date_bytes(self, file_ptr):
        # creation date extraction logic
        self.date_string = datetime.datetime.strftime(datetime.datetime.now(), format="%d/%m/%Y %H:%M")
        self.extract_date_format()
        return file_ptr, self.extract_datetime()

    def extract_date_format(self):
        self.date_format = "%d/%m/%Y %H:%M"

    def extract_datetime(self):
        return datetime.datetime.strptime(self.date_string, self.date_format)

class InvoiceFloatHandler():
    @staticmethod
    def extract_float(file_ptr):
        return file_ptr, 1000.0



class MockInvoiceItemGenerator():
    def __init__(self, invoice):
        self.vendor_items = VendorItem.objects.filter(vendor=invoice.vendor)
        self.invoice = invoice

    def generate_data(self):
        result = []
        for i, item in enumerate(self.vendor_items):
            invoice_item = self.get_invoice_item_from_vendor_item(item, i+1)
            result.append(invoice_item)
        return result
    def get_invoice_item_from_vendor_item(self, vendor_item, serial_no):
        invoice_item = InvoiceItem(item=vendor_item)
        invoice_item.quantity = CommonUtils.generate_random_int(1, 10)
        invoice_item.unit_price = CommonUtils.generate_random_int(10, 100)
        invoice_item.total_cost = invoice_item.quantity * invoice_item.unit_price
        invoice_item.invoice = self.invoice
        invoice_item.serial_no = serial_no
        invoice_item.save()
        return invoice_item




