"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""
from dataclasses import dataclass
from environs import Env

# https://yandex.ru/support/mail/mail-clients/others.html


@dataclass
class MailConfig:
    user: str
    password: str
    host: str
    port: int


@dataclass
class Config:
    mail: MailConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        mail=MailConfig(
            user=env('SMTP_USER'),
            password=env('SMTP_PASSWORD'),
            port=env('SMTP_PORT'),
            host=env('SMTP_HOST')
        )
    )
