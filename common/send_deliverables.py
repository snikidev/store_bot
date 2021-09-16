import boto3
from common.settings import Settings

settings = Settings()

s3 = boto3.client(
    service_name="s3",
    region_name="eu-west-1",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def send_deliverables(bot, message):
    folder = message.successful_payment.invoice_payload
    print(folder)
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

        bot.send_message(
            message.chat.id,
            """{}/{}  
            🇬🇧 Follow [this link]({}) to download the product. Download will start automatically. The link will be available for the next 48 hours. 
              
            🇷🇺 Пройдите по [этой ссылке]({}), чтобы скачать продукт. Скачивание начнется автоматически. Ссылка будет доступна в течении следующих 48 часов.  
            """.format(
                index + 1, len(deliverables), url, url
            ),
        )

    return deliverables
