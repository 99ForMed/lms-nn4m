from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

class CustomS3Storage(S3Boto3Storage):
    def get_available_name(self, name, max_length=None):
        """
        Override the method to remove the unnecessary file existence check.
        """
        if max_length and len(name) > max_length:
            raise(ValueError("File name too long."))
        return name