import que
from datetime import datetime, timedelta, timezone
from user import User
from change_time import change_time_p
import threading
from util import Util
import time

def auto_change_time_1_min(username, passwd, email, start1, start2, start3, end, room_id, seat_no):


    usr = User(username, passwd, email)
    usr.get_token()
    flag, a, aa, start, end = usr.reservation_reserve_status()
    start =  datetime.strptime(start, '%H:%M')
    start = (start + timedelta(minutes=30)).strftime("%H:%M")

    if not flag:
        print('没有有效预约')
        return

    if should_change(start):
        print('should change')
        if Util.time_compare(start2,Util.get_cn_now()):
            change_time_p(usr, room_id, seat_no=seat_no, start=Util.str_time_to_float(start2), end=Util.str_time_to_float(end))
        elif Util.time_compare(start3,Util.get_cn_now()):
            change_time_p(usr, room_id, seat_no=seat_no, start=Util.str_time_to_float(start3), end=Util.str_time_to_float(end))
        else:
            usr.stop_cancel()




def should_change(startx):
    format_pattern = '%H:%M'
    now = get_cn_now()
    diff = (datetime.strptime(startx, format_pattern) - datetime.strptime(now, format_pattern))
    flag = datetime.strptime('01:02', format_pattern) - datetime.strptime('01:01', format_pattern)
    if diff == flag:
        return True
    else:
        return False


# 返回str的当前cn时区时间 '%H:%M'
def get_cn_now():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    format_pattern = '%H:%M'
    cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    now = cn_dt.strftime(format_pattern)
    return now


def main():
    # 如果当前时间不是7~21点，则不需要检测换时间
    if not (Util.time_compare(Util.get_cn_now(), '07:00') and Util.time_compare('21:00', Util.get_cn_now())):
        return
    print(time.localtime())

    threads = []
    for u in que.users:
        username = u.get('username')
        passwd = u.get('password')
        email = u.get('email')
        start1 = u.get('start1')
        end1 = u.get('end1')
        start2 = u.get('start2')
        end2 = u.get('end2')
        start3 = u.get('start3')
        end3 = u.get('end')
        room_id = u.get('room_id')
        seat_no = u.get('seat_no')
        t1 = threading.Thread(target=auto_change_time_1_min,
                              args=(username, passwd, email, start1, start2, start3, end3, room_id, seat_no))
        threads.append(t1)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
