import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import logging
from typing import Optional

from config.config import load_config


mail_logger = logging.getLogger('utils_logger')
mail_config = load_config(None).mail


def send_email(receiver: str,
               order_id: Optional[str] = None, images: Optional[list[str]] = None):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    mail_logger.info(f'Starting sending email;\nreceiver: {receiver}\norder_id: {order_id}\nimages: {images}')

    try:
        with smtplib.SMTP_SSL(mail_config.host, mail_config.port) as server:
            server.login(user=mail_config.user, password=mail_config.password)
            mail_logger.debug('Authorization was successful')

            email = MIMEMultipart()
            email['From'] = mail_config.user
            email['To'] = receiver
            email['Subject'] = f'Еженедельная рассылка. Письмо о сервисе.'

            email.attach(MIMEText('Письмо о сервисе "Заработай, пожалуйста"', 'plain'))
            if order_id:
                email['Subject'] += f' Изображения. Заказ №{order_id}'

                if images:
                    for image in images:
                        mail_logger.debug(f'image: {image}')
                        with open(image, 'rb') as attachment:
                            mail_logger.debug(f'Opened image: {str(attachment)}')
                            img = MIMEImage(attachment.read())
                            img.add_header('Content-Disposition', 'attachment', filename=image)
                            email.attach(img)
                            # part = MIMEBase('application', 'octet-stream')
                            # part.set_payload(attachment.read())
                            #
                            # encoders.encode_base64(part)
                            # part.add_header(
                            #     'Content-Disposition',
                            #     f'attachment; filename={image}'
                            # )
                            # email.attach(part)

            # text = email.as_string()
            # server.sendmail(mail_config.user, receiver, text)

            server.send_message(email)
            mail_logger.info('Email was sent')
    except Exception as exc:
        mail_logger.exception('Error sending email', exc_info=exc)


if __name__ == '__main__':
    send_email(mail_config.user, '...', ['./static/blured_images/2.png'])
