import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime


def emailBySMTP(host, port, user, pw, sender, receivers, content):

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = receivers[0]

    message['Subject'] = '%s日程提醒' % datetime.date.today()

    try:
        mailBox = smtplib.SMTP_SSL(host)
        mailBox.connect(host=host, port=port)
        mailBox.login(user, pw)
        mailBox.sendmail(sender, receivers, message.as_string())
        mailBox.quit()

        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败：\n', e)


if __name__ == '__main__':
    emailBySMTP('smtp.189.cn', 465, 'metorm', 'WhyAmISoSmart',
                'metorm#189.cn', ['metorm#126.com'], 'This is a test email.')
