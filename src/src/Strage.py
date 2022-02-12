import boto3
import os

class Strage:
    def __init__(self, bucket_name):
        self.bucket = boto3.resource('s3').Bucket(bucket_name)

    def upload(self, file_path):
        file_name = os.path.basename(file_path)
        self.bucket.upload_file(file_path, file_name)

    def download(self, key):
        self.bucket.download_file(key, key)