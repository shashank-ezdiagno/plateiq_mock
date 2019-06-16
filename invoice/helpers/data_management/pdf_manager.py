from django.conf import settings
from .s3_manager import S3Manager, S3ObjectType
import datetime
import hashlib
import os

class S3PDFManager(object):
    s3_object_type = S3ObjectType.PDF
    def __init__(self, buyer_id):
        self.buyer_id = buyer_id

    def save(self, file_name, data):
        pdf_path_folder = self.buyer_id
        s3_manager = S3Manager(self.__class__.s3_object_type)
        pdf_path = os.path.join(pdf_path_folder, file_name)
        s3_manager.put_object(pdf_path, data)
        return pdf_path

    def get(self, file_name):
        pdf_path = os.path.join(self.buyer_id, file_name)
        s3_manager = S3Manager(self.__class__.s3_object_type)
        return s3_manager.get_object(pdf_path)

    def delete(self, file_name):
        pdf_path = os.path.join(self.buyer_id, file_name)
        s3_manager = S3Manager(self.__class__.s3_object_type)
        return s3_manager.delete_object(pdf_path)

class PDFHandler(object):
    def __init__(self, buyer_id):
        hash_buyer_id = hashlib.sha1(buyer_id.encode('utf-8')).hexdigest()
        self.manager = PDFHandler.get_pdf_manager(hash_buyer_id)

    def save(self, name, data):
        hash_name = hashlib.sha1(name.encode('utf-8')).hexdigest()
        pdf_path = self.manager.save(hash_name, data)
        return hash_name

    def get(self, name):
        hash_name = hashlib.sha1(name.encode('utf-8')).hexdigest()
        return self.manager.get(hash_name)

    def delete(self, name):
        hash_name = hashlib.sha1(name.encode('utf-8')).hexdigest()
        return self.manager.delete(hash_name)

    @staticmethod
    def get_pdf_manager(hash_buyer_id):
        return S3PDFManager(hash_buyer_id)