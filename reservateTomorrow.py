import user
import datetime
import util
import time
import datetime



def reservate_tommorow(roomId=7,seat_no=41,start=9,end=17):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    howard = user.User('2015301020142','17871X')
    cs = user.User('2015302590161','180010')
    howard.get_token()
    cs.get_token()

    reservate_result_hw,location_hw = howard.reservate(roomId,seat_no,str(tomorrow),start,end)
    reservate_result_cs,location_cs = cs.reservate(roomId,seat_no+10,str(tomorrow),start,end)

    if reservate_result_cs == True:
        util.Util.sendMail('245015259@qq.com',location_cs,str(start)+'->'+str(end))
    if reservate_result_hw == True:
        util.Util.sendMail('837971940@qq.com',location_hw,str(start)+'->'+str(end))

def change_time(roomId=7,seat_no=41,start=14.5,end=17):
    today = datetime.date.today()
    
    howard = user.User('2015301020142','17871X')
    cs = user.User('2015302590161','180010')
    howard.get_token()
    cs.get_token()

    howard.stop_cancel()
    reservate_result_hw,location_hw = howard.reservate(roomId,seat_no,str(today),start,end)
    cs.stop_cancel()
    reservate_result_cs,location_cs = cs.reservate(roomId,seat_no+10,str(today),start,end)

    if reservate_result_cs == True:
        util.Util.sendMail('245015259@qq.com',location_cs,str(start)+'->'+str(end))
    else:
        reservate_result_cs,location_cs = cs.reservate_exclude(roomId,today,start,end)
        if reservate_result_cs == True:
            util.Util.sendMail('245015259@qq.com',location_cs,str(start)+'->'+str(end))
    
    if reservate_result_hw == True:
        util.Util.sendMail('837971940@qq.com',location_hw,'9 -> 17')
    else:
        reservate_result_hw,location_hw = hw.reservate_exclude(roomId,today,start,end)
        if reservate_result_hw == True:
            util.Util.sendMail('837971940@qq.com',location_hw,str(start)+'->'+str(end))

    

def test():
    today = datetime.date.today()
    howard = user.User('2015301020142','17871X')
    howard.get_token()
    howard.stop_cancel()
    howard.reservate(7,29,str(today),12,13.5)


if __name__ == '__main__':

    reservate_tommorow()
    

    # test()
    # command = input('1 reservate today\n2 reservate tomorrow\n')
    # function_select(command)






