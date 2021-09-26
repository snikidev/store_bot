import boto3
from common.settings import Settings
from common.dictionary import dictionary

settings = Settings()

s3 = boto3.client(
    service_name="s3",
    region_name="eu-west-1",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def send_deliverables(bot, message):
    folder = message.successful_payment.invoice_payload
    language_code = message.from_user.language_code

    all_objects = s3.list_objects_v2(
        Bucket=settings.s3_bucket_name, Prefix=folder + "/", MaxKeys=100
    )

    deliverables = [
        deliverable
        for deliverable in all_objects["Contents"]
        if deliverable["Key"][-1] != "/"
    ]

    for index, obj in enumerate(deliverables):
        # Get last part of the s3 key == actual filename
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket_name, "Key": obj["Key"]},
            ExpiresIn=172800,
        )

        message_text = dictionary[language_code].deliverable_message.format(
            index + 1, len(deliverables), url, url
        )

        bot.send_message(message.chat.id, message_text)

    return deliverables
