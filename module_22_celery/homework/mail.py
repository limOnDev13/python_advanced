import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from config.config import MailConfig


def send_email(order_id: str, receiver: str, images: list[str], mail_config: MailConfig):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    with smtplib.SMTP(mail_config.host, mail_config.port) as server:
        server.starttls()
        server.login(mail_config.user, mail_config.password)

        email = MIMEMultipart()
        email['Subject'] = f'Изображения. Заказ №{order_id}'
        email['From'] = mail_config.user
        email['To'] = receiver

        for image in images:
            with open(image, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={image}'
            )
        email.attach(part)
        text = email.as_string()

        server.sendmail(mail_config.user, receiver, text)
