#coding:utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import make_header
from email import encoders


def sendemail(subject, body, attachments=None, fromaddr=None, toaddr=None, pwd=None):
    try:
        f = open("account.txt", "r")
        default_addr = f.readline()
        default_pwd = f.readline()
        f.close()
    except FileNotFoundError:
        default_addr = None
        default_pwd = None
        pass

    if fromaddr is None:
        fromaddr = default_addr

    if toaddr is None:
        toaddr = default_addr

    if pwd is None:
        pwd = default_pwd

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', _charset='UTF-8'))

    # attachment
    if attachments is not None:
        for attachment_path in attachments:
            attachment = open(attachment_path, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' %
                            make_header([(attachment_path.split('/')[-1], 'UTF-8')]).encode('UTF-8'))
            msg.attach(part)
            attachment.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
