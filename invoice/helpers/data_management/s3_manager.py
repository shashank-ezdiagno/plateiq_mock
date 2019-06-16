import boto3
from django.conf import settings
from enum import IntEnum
import os
import logging

logger = logging.getLogger(__name__)

class S3ObjectType(IntEnum):
    PDF = 0

    def from_str(str):
        return {
            'pdf' : S3ObjectType.PDF,
        }.get(str, S3ObjectType.PDF)

    def __str__(self):
        return {
            S3ObjectType.PDF : 'pdf',
        }.get(self, 'pdf')

    def get_s3_path_prefix_and_key(self):
        default_return = (settings.S3_PDF_PREFIX, settings.S3_KEY)
        return {
            S3ObjectType.PDF : (settings.S3_PDF_PREFIX, settings.S3_KEY)
        }.get(self, default_return)



class S3Manager():
    def __init__(self, object_type):
        self.path_prefix, self.encrypt_key = object_type.get_s3_path_prefix_and_key()
        self.client = settings.S3_CLIENT

    def put_object(self, path, file_object):
        logger.info("Put object... - %s", path)
        path = os.path.join(self.path_prefix, path)
        print(path)
        self.client.put_object(Bucket=settings.S3_BUCKET,
                      Key=path, Body=file_object,
                      ServerSideEncryption='aws:kms',
                      SSEKMSKeyId=self.encrypt_key)
        print("Done")

    def get_object(self, path):
        # Getting the object:
        logger.info("Getting object... - %s", path)
        path = os.path.join(self.path_prefix, path)
        response = self.client.get_object(Bucket=settings.S3_BUCKET,
                                 Key=path)
        return response['Body']

    def delete_object(self, path):
        logger.info("deleting object... - %s", path)
        path = os.path.join(self.path_prefix, path)
        self.client.delete_object(
                                 Bucket=settings.S3_BUCKET,
                                 Key=path
                                )


