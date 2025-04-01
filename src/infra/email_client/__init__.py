import smtplib
from typing import Union
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.infra.logi import logger
class EmailClient:

    def __init__(self,
                 email: str,
                 password: str,
                 smtp_host: str,
                 smtp_port: int):
        self.email = email
        self.password = password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.server: Union[None, smtplib.SMTP] = None

    def connect(self):
        if self.server is None:
            try:
                self.server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                self.server.starttls()
                self.server.login(self.email, self.password)
            except Exception as e:
                logger.warning(f'SMTP CONN EROR [{e}]')

    def close(self):
        if self.server is not None:
            self.server.quit()

    def send_email(self, receiver_email, title, body) -> bool:
        self.connect()
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = receiver_email
            msg['Subject'] = title
            msg.attach(MIMEText(body, 'plain'))
            self.server.sendmail(self.email, receiver_email, msg.as_string())
            return True
        except Exception as e:
            return False


email_client = EmailClient(
    email='zull4n06@gmail.com',
    password="asmf qgog nivb eqek",
    smtp_host="smtp.gmail.com",
    smtp_port=587
)
