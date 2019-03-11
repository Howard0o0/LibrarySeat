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
        usr.loop_reservate()
 
    
def test():
    today = datetime.date.today()
    howard = user.User('2015301020142', '17871X', '837971940')
    howard.get_token()

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
        t1 = threading.Thread(target=auto_change_time,
                              args=(username, passwd, email, end1, start2, end2, start3, end3, room_id, seat_no))
        threads.append(t1)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()




if __name__ == '__main__':
    print(time.localtime())

    main()

    # usr = user.User('2015301020142','17871X','245015259@qq.com')
    # change_time_p(usr,seat_no=51,start=16,end=18)

    print('time is up!')










