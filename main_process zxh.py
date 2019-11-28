import user
import datetime
import util
import time
import datetime
import threading
import que
from util import Util

cnt = 0


def reservate_tomorrow_p(user,roomId=6,seat_no=50,start=9,end=17):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if user.rtn_token() == None:
        user.get_token()

    user.reservate(roomId, seat_no, str(tomorrow), start, end)
    hw_rs, _, __ ,___,begin,end= user.reservation()
    if hw_rs == True:
        return

    for i in range(5):
        if hw_rs == True:
            return
        msg = user.get_username() + str(hw_rs)
        util.Util.sendMail('837971940@qq.com','reservate_tomorrow error'+ str(i) +':'+msg)
        time.sleep(1)
        hw_rs,_ = user.reservate(roomId, seat_no, str(tomorrow), start, end)
        if hw_rs == True:
            return
        hw_rs, _ = user.reservate_exclude(roomId,str(tomorrow),start,end)

def main():
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
        usr = user.User(username,passwd,email)
        usr.get_token()
        t1 = threading.Thread(target=reservate_tomorrow_p,
                              args=(usr, room_id,seat_no,Util.str_time_to_float(start1),Util.str_time_to_float(end3)))
        threads.append(t1)

    Util.wait_until_rsvtime()

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()
        
def test():

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    zxh = user.User('2015301610164','210013','695977846@qq.com')

    Util.wait_until_rsvtime()
        
    res,loc = zxh.reservate(roomId=7, seat_no=84, date=str(tomorrow), start=9, end=21)
    if(res == False):
        zxh.reservate_exclude( 7, str(tomorrow), 9, 21)


if __name__ == '__main__':


    test()






