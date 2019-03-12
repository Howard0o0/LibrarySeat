from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import time
from datetime import datetime, timedelta, timezone


class Util:

    @classmethod
    def sendMail(cls, rec, mail_msg):
        mail_server = 'smtp.qq.com'
        port = '25'
        sender_qq = '837971940'
        sender_passwd = 'cwfxivexhmgabdfc'
        send_qq_mail = '837971940@qq.com'
        receiver = rec
        msg = MIMEText(mail_msg, 'plain', 'utf-8')
        msg['From'] = send_qq_mail
        msg['To'] = receiver
        msg['Subject'] = Header('Reservation Result', 'utf-8')

        try:
            smtp = SMTP_SSL(mail_server)
            smtp.ehlo(mail_server)
            smtp.login(sender_qq, sender_passwd)
            smtp.sendmail(send_qq_mail, receiver, msg.as_string())
            smtp.quit()  # 断开连接
            print("邮件发送成功！")
        except:
            smtp.quit()
            print("邮件发送失败！")


    @classmethod
    def time_cmp(cls, first_time, second_time):
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

    # if str_time1 > str_time2,return True
    @classmethod
    def time_compare(cls, str_time1, str_time2):
        format_pattern = '%H:%M'
        time1 = datetime.strptime(str_time1, format_pattern)
        time2 = datetime.strptime(str_time2, format_pattern)
        pattern_2 = '%H%M'
        str_t1 = datetime.strftime(time1,pattern_2)
        str_t2 = datetime.strftime(time2, pattern_2)
        diff = (int(str_t1) -  int(str_t2))
        if diff > 0:
            return True
        else:
            return False



    @classmethod
    def should_change(cls, startx):
        format_pattern = '%H:%M'
        now = cls.get_cn_now()
        diff = (datetime.strptime(startx, format_pattern) - datetime.strptime(now, format_pattern))
        flag = datetime.strptime('01:02', format_pattern) - datetime.strptime('01:01', format_pattern)
        if diff == flag:
            return True
        else:
            return False

    @classmethod
    def get_cn_now(cls):
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        format_pattern = '%H:%M'
        cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        now = cn_dt.strftime(format_pattern)
        return now

    @classmethod
    def str_time_to_float(cls, str_time):
        str_hour = str_time[0:2]
        str_min = str_time[3:]
        hour = float(str_hour)
        if str_min == '30':
            hour = hour + 0.5
        return hour
