#coding:utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import make_header
from email import encoders

class emailClient:
    def __init__(self, fromaddr=None, toaddr=None, pwd=None):
        try:
            f = open("account.txt", "r")
            default_toaddr = f.readline()
            default_fromaddr = f.readline()
            default_pwd = f.readline()
            f.close()
        except FileNotFoundError:
            default_fromaddr = None
            default_toaddr = None
            default_pwd = None
            pass

        self.fromaddr = default_fromaddr if fromaddr is None else fromaddr
        self.toaddr = default_toaddr if toaddr is None else toaddr
        self.pwd = default_pwd if pwd is None else pwd

        assert self.fromaddr != None and self.toaddr != None and self.pwd != None

    def sendemail(self, subject, body, attachments=None, toaddr=None):
        curr_toaddr = toaddr if toaddr is not None else self.toaddr
        print('Sending to %s' % curr_toaddr)
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = curr_toaddr
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain', _charset='UTF-8'))

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
        server.login(self.fromaddr, self.pwd)
        text = msg.as_string()
        server.sendmail(self.fromaddr, curr_toaddr, text)
        server.quit()
