from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


class Util:

    @classmethod
    def sendMail(self,rec,mail_msg):
        mail_server = 'smtp.qq.com'
        port = '25'
        sender_qq = '837971940'
        sender_passwd = 'cwfxivexhmgabdfc'
        send_qq_mail = '837971940@qq.com'
        receiver = rec
        msg = MIMEText(mail_msg,'plain','utf-8')
        msg['From'] = send_qq_mail
        msg['To'] = receiver
        msg['Subject'] = Header('Reservation Result','utf-8')

        try:
            smtp = SMTP_SSL(mail_server)
            smtp.ehlo(mail_server)
            smtp.login(sender_qq,sender_passwd)
            smtp.sendmail(send_qq_mail,receiver,msg.as_string())
            smtp.quit()  # 断开连接
            print("邮件发送成功！")
        except:
            smtp.quit()
            print("邮件发送失败！")





