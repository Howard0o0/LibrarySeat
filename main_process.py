import user
import datetime
import util
import time
import datetime
import threading

cnt = 0


def reservate_tomorrow_p(user,roomId=6,seat_no=50,start=9,end=17):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    if user.rtn_token() == None:
        user.get_token()

    user.reservate(roomId, seat_no, str(tomorrow), start, end)
    hw_rs, _, __ = user.reservation()
    if hw_rs == True:
        return

    for i in range(5):
        if hw_rs == True:
            return
        msg = user.get_username() + str(hw_rs)
        util.Util.sendMail('837971940@qq.com','reservate_tomorrow error'+ str(i) +':'+msg)
        time.sleep(1)
        user.reservate(roomId, seat_no, str(tomorrow), start, end)
        user.reservate_exclude(roomId,str(tomorrow),start,end)

if __name__ == '__main__':
    print(time.localtime())

    howard = user.User(username='2015301020142',password='17871X',mail='837971940@qq.com')
    cs = user.User(username='2015302590161',password='180010',mail='245015259@qq.com')
    howard.get_token()
    cs.get_token()


    threads = []
    t1 = threading.Thread(target=reservate_tomorrow_p,args=(howard,6,50,9,17))
    threads.append(t1)
    t2 = threading.Thread(target=reservate_tomorrow_p, args=(cs, 6, 52, 9,17))
    threads.append(t2)

    util.Util.wait_until_rsvtime()


    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    # test()
    # command = input('1 reservate today\n2 reservate tomorrow\n')
    # function_select(command)






