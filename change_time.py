# -*- coding: utf-8 -*-

import user
import datetime
import util
import time
import datetime
import sys
import threading
import que
from util import Util

def auto_change_time(username,passwd,email,end1,start2,end2,start3,end3,room_id,seat_no):
    usr = user.User(username,passwd,email)
    end3 = Util.str_time_to_float(end3)
    str_now =  Util.get_cn_now()
    flag,status,a,aa,aaa,aaaa = usr.reservation()
    if flag and (status == 'CHECK_IN'or status == 'AWAY'):
        #中午换时间
        if Util.time_compare(str_now,end1) and Util.time_compare(start2,str_now):
            s2 = Util.str_time_to_float(start2)
            print('s2:',s2)
            change_time_p(usr,room_id,seat_no,s2,end3)
        #下午换时间
        if Util.time_compare(str_now,end2) and Util.time_compare(start3,str_now):
            s3 = Util.str_time_to_float(start3)
            change_time_p(usr,room_id,seat_no,s3,end3)



def change_time_p(usr,roomId=6,seat_no=50,start=14.5,end=17):
    today = datetime.date.today()
    usr.get_token()
    usr.stop_cancel()
    reservate_result_hw, location_hw = usr.reservate(roomId, seat_no, str(today), start, end)
    if reservate_result_hw == False:
        usr.loop_reservate(roomId, seat_no, start, end)
 

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
        t1 = threading.Thread(target=auto_change_time,
                              args=(username, passwd, email, end1, start2, end2, start3, end3, room_id, seat_no))
        threads.append(t1)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()


def test():
    howard = user.User('2019282110139','17871X','695977846@qq.com')
    howard.get_token()
    # howard.stop_cancel()
    howard.reservate_ssq(roomId=6,seat_no=84,start=19,end=21)
    howard.loop_reservate(roomId=6, seat_no=84, start=19, end=21)

if __name__ == '__main__':

    # main()
    test()











