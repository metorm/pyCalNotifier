import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import time


def emailBySMTP(host, port, user, pw, sender, receivers, content, retries, retryInterval):

    assert isinstance(retries, int)
    assert isinstance(retryInterval, int)

    content += ("\n发送于：" + str(datetime.datetime.now()))

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = receivers[0]

    message['Subject'] = '%s待办提醒：共%d项' % (
        datetime.date.today(), content.count('>'))

    mail_success = False
    for tries in range(1, retries+1):
        if mail_success:
            break

        print("第%d次尝试发送邮件……" % tries)

        try:
            mailBox = smtplib.SMTP_SSL(host)
            mailBox.connect(host=host, port=port)
            mailBox.login(user, pw)
            mailBox.sendmail(sender, receivers, message.as_string())
            mailBox.quit()

            mail_success = True

            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败：\n', e)
            time.sleep(retryInterval)


if __name__ == '__main__':
    emailBySMTP('smtp.189.cn', 465, 'metorm', 'WhyAmISoSmart',
                'metorm#189.cn', ['metorm#126.com'], 'This is a test email.')
