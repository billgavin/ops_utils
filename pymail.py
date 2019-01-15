from email import encoders
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from template import html, img

import jinja2
import hashlib
import os
import smtplib
import mimetypes

html = u'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
　　<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
　　<title>{{title}}</title>
　　<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<table border="0" cellpadding="0" cellspacing="0" width="100%">
    {%- for part in contents %}
    <tr><td>{{part}}</td></tr>
    {%- endfor %}
<table>
</html>
        '''

img = u'''
<img src="cid:{{imageid}}" alt="{{image}}">
'''

class Server():
    
    def __init__(self, server='localhost', user='', password='', port=25, debug=False, tls=False):
        self.mail = smtplib.SMTP(server, port)
        if debug: self.mail.set_debuglevel(1)
        if tls: self.mail.starttls()
        if user and password: self.mail.login(user, password)
        self.from_addr = user

    def send(self, to_addrs, message):
        self.mail.sendmail(self.from_addr, to_addrs, message.as_string())
        self.mail.quit()
        

class Message():
    
    def __init__(self, from_addr, to_addrs, subject, cc_addrs=None, bcc_addrs=None):
        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = from_addr
        self.msg['To'] = ','.join(to_addrs)
        self.msg['Subject'] = subject
        self.to_addrs = to_addrs 
        if cc_addrs:
            self.msg['Cc'] = ','.join(cc_addrs)
            self.to_addrs += cc_addrs
        if bcc_addrs:
            self.msg['Bcc'] = ','.join(bcc_addrs)
            self.to_addrs += bcc_addrs

    def text_msg(self, text):
        self.msg.attach(MIMEText(text, 'plain', 'utf-8'))
        return self.msg

    def html_msg(self, *parts):
        title = self.msg['Subject']
        content = self.render(html, title=title, contents=parts)
        self.msg.attach(MIMEText(content, 'html', 'utf-8'))
        return self.msg

    def attach_msg(self, *attach_files):
        imgs = []
        for attach_file in attach_files:
            mime_type, encoding = mimetypes.guess_type(attach_file)
            mime_type = mime_type if mime_type else 'text/plain'
            main_type, sub_type = mime_type.split('/')
            filename = os.path.basename(attach_file)
            with open(attach_file) as f:
                file_context = f.read()
            md5_id = hashlib.md5(file_context).hexdigest()

            mime = MIMEBase(main_type, sub_type, filename = filename)
            mime.add_header('Content-Disposition', 'attachment', filename = filename)
            mime.add_header('Content-ID', '<%s>' % md5_id)
            mime.add_header('X-Attachment-Id', md5_id)
            mime.set_payload(file_context)
            encoders.encode_base64(mime)
            self.msg.attach(mime)
            if main_type == 'image':
                img_html = self.render(img, imageid=md5_id, image=filename)
                imgs.append(img_html)
        if imgs: return imgs        


    def render(self, template, **kws):
        temp = jinja2.Template(source=template)
        res = temp.render(kws)
        return res

