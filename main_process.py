import user
import datetime
import util
import time
import datetime

cnt = 0

def reservate_tommorow(roomId=7,seat_no=41,start=9,end=17):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    howard = user.User('2015301020142','17871X','879791940@qq.com')
    cs = user.User('2015302590161','180010','245015259@qq.com')
    howard.get_token()
    cs.get_token()

    howard.reservate(roomId,seat_no,str(tomorrow),start,end)
    cs.reservate(roomId,seat_no+10,str(tomorrow),start,end)

    hw_rs,_,__ = howard.reservation()
    cs_rs,a,aa = cs.reservation()

    while cnt <= 5 and (hw_rs == False or cs_rs == False):
        ++cnt
        msg = 'hw:' + str(hw_rs) + ' ,cs:' + str(cs_rs)
        util.Util.sendMail('837971940@qq.com','reservate_tomorrow error'+ str(cnt) +':'+msg)
        if cnt <= 5:
            time.sleep(3)
            reservate_tommorow()






def change_time(roomId=7,seat_no=41,start=14.5,end=17):
    today = datetime.date.today()
    
    howard = user.User('2015301020142','17871X',"837971940@qq.com")
    cs = user.User('2015302590161','180010',"245015259@qq.com")
    howard.get_token()
    cs.get_token()

    howard.stop_cancel()
    reservate_result_hw,location_hw = howard.reservate(roomId,seat_no,str(today),start,end)
    cs.stop_cancel()
    reservate_result_cs,location_cs = cs.reservate(roomId,seat_no+10,str(today),start,end)

   

    

def test():
    today = datetime.date.today()
    howard = user.User('2015301020142','17871X','837971940@qq.com')
    howard.get_token()
    howard.stop_cancel()
    howard.reservate(7,29,str(today),12,13.5)


if __name__ == '__main__':
    reservate_tommorow()
    

    # test()
    # command = input('1 reservate today\n2 reservate tomorrow\n')
    # function_select(command)






