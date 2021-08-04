import boto3
import os
from common.settings import Settings

settings = Settings()

s3 = boto3.resource(
    service_name="s3",
    region_name="eu-west-1",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def send_deliverables(bot, message, folder):
    deliverables = s3.Bucket(settings.s3_bucket_name).objects.filter(
        Prefix=folder + "/"
    )

    for obj in deliverables:
        # Get last part of the s3 key == actual filename
        filename = str(obj.key.split("/")[-1])
        if filename != "":
            s3.Bucket(settings.s3_bucket_name).download_file(obj.key, filename)
            file = open("./{}".format(filename), "rb")
            bot.send_document(message.chat.id, file, timeout=20)

            # Clean out all the files from the instance
            os.remove(filename)

    return deliverables
