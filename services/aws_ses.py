import boto3
from botocore.exceptions import ClientError
from decouple import config


class SESService():
    def __init__(self):
        key = config("AWS_KEY")
        secret = config("AWS_SECRET_KEY")
        region = config("S3_REGION")

        self.ses = boto3.client(
            "ses",
            region_name=region,
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )
        self.sender = "aleksandra.angelova2@gmail.com"

    def send_email(self, recipient, transaction_details):
        SUBJECT = "MTG Card Trading: New trade request"

        BODY_TEXT = (
            "MTG Card Trading: New trade request"
            "You have a new card trade request. Log in to your account "
            "to approve or reject it "
            f"Details: {transaction_details}"
        )

        # The HTML body of the email.
        BODY_HTML = f"""<html>
        <head></head>
        <body>
          <h1>MTG Card Trading: New trade request</h1>
          <p>You have a new card trade request. Log in to your account 
          to approve or reject it. Details: {transaction_details}
            </p>
        </body>
        </html>
                    """
        CHARSET = "UTF-8"

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = self.ses.send_email(
                Destination={
                    "ToAddresses": [
                        recipient,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": CHARSET,
                            "Data": BODY_HTML,
                        },
                        "Text": {
                            "Charset": CHARSET,
                            "Data": BODY_TEXT,
                        },
                    },
                    "Subject": {
                        "Charset": CHARSET,
                        "Data": SUBJECT,
                    },
                },
                Source=self.sender
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])


if __name__ == "__main__":
    ses_client = SESService()
    ses_client.send_email(recipient="silly.monkey200@gmail.com", transaction_details={})

