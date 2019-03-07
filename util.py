from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import time


class Util:

    @classmethod
    def sendMail(cls,rec,mail_msg):
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

    @classmethod
    def time_cmp(cls,first_time, second_time):
        # print(first_time)
        # print(second_time)
        return int(time.strftime("%H%M%S", first_time)) - int(time.strftime("%H%M%S", second_time))

    # 如果现在是预约时间，返回TRUE否则返回FALSE
    @classmethod
    def is_rsv_time(cls):
        rsv_time = time.strptime("22:45:00", '%H:%M:%S')
        now = time.localtime()
        result = cls.time_cmp(now, rsv_time)
        if result < 0:
            return False
        else:
            return True

    @classmethod
    def wait_until_rsvtime(cls):
        while True:
            is_rsv_time = cls.is_rsv_time()
            if is_rsv_time:
                print('time is up!')
                break





