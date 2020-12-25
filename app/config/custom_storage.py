from storages.backends.s3boto3 import S3Boto3Storage
# environment variables
import os
from django.conf import settings
import environ


# environ
env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))
# get bucket name
s3_name = env('AWS_STORAGE_BUCKET_NAME')


# media
class MediaStorage(S3Boto3Storage):
    # S3のディレクトリを指定
    location = settings.MEDIA_LOCATION
    # bucketの名前
    bucket_name = s3_name
    # fileが重複しても、上書きしない
    file_overwrite = False
