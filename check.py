import user
import que
from datetime import datetime
from datetime import datetime, timedelta, timezone
from user import User
from change_time import change_time_p
import threading


def auto_change_time_1_min(username, passwd, email, start1, start2, start3, end, room_id, seat_no):
    start1 = datetime.strptime(start1, '%H:%M')
    start1 = (start1 + timedelta(minutes=30)).strftime("%H:%M")
    start2 = datetime.strptime(start2, '%H:%M')
    start2 = (start1 + timedelta(minutes=30)).strftime("%H:%M")
    start3 = datetime.strptime(start3, '%H:%M')
    start3 = (start1 + timedelta(minutes=30)).strftime("%H:%M")

    usr = User(username, passwd, email)
    usr.get_token()
    flag, a, aa, start, end = usr.reservation_reserve_status()
    if not flag:
        return

    if should_change(start1):
        change_time_p(usr, room_id, seat_no=seat_no, start=start2, end=end)
    if should_change(start2):
        change_time_p(usr, room_id, seat_no=seat_no, start=start3, end=end)
    if should_change(start3):
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
        t1 = threading.Thread(target=auto_change_time_1_min(),
                              args=(username, passwd, email, start1, start2, start3, end3, room_id, seat_no))
        threads.append(t1)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
