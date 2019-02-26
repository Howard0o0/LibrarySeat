import user
import datetime
import util
import time
import datetime

def reservate_today():
    user_name = input('å­¦å·:')
    passwd = input('å¯ç :')
    print(type(user_name),type(passwd))
    user1 = user.User(user_name,password=passwd)
    user1.get_token()
    seated,b,c = user1.reservation()
    if seated == True:
        print('å·²æä¸ä¸ªææé¢çº¦å¦')
    room_id = int(input('room id selected: 6(äºæ¥¼è¥¿) 7(äºæ¥¼ä¸) 8ï¼ä¸æ¥¼è¥¿ï¼ 10ï¼ä¸æ¥¼ä¸ï¼'))
    start = float(input('start time:'))
    end = float(input('end time:'))
    seat_no = input('åº§ä½å·:')
    user1.stop_cancel()
    today = str(datetime.date.today())
    result = user1.reservate(today,room_id,seat_no,start,end)
    if result == False:
        user1.reservate_exclude(room_id,today,start,end)

def reservate_tommorow():
    pass

def function_select(argument):
    switcher = {
        1: reservate_today(),
        2: reservate_tommorow()
    }

def main():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    howard = user.User('2015301020142','17871X')

    cs = user.User('2015302590161','180010')
    howard.get_token()
    cs.get_token()

    reservate_result_hw,location_hw = howard.reservate(6,27,str(tomorrow),9,21)
    reservate_result_cs,location_cs = cs.reservate(6,29,str(tomorrow),9,21)

    if reservate_result_cs == True:
        util.Util.sendMail('245015259@qq.com',location_cs)
    if reservate_result_hw == True:
        util.Util.sendMail('837971940@qq.com',location_hw)

def test():
    today = datetime.date.today()
    howard = user.User('2015301020142','17871X')
    howard.get_token()
    howard.stop_cancel()
    howard.reservate(7,29,str(today),12,13.5)


if __name__ == '__main__':

    main()

    # test()
    # command = input('1 reservate today\n2 reservate tomorrow\n')
    # function_select(command)






