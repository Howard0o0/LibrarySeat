import user
import datetime
import util
import time
import datetime
import sys





def change_time(roomId=6,seat_no=67,start=14.5,end=17):
    today = datetime.date.today()
    
    
    howard = user.User('2015301020142','17871X',"837971940@qq.com")
    cs = user.User('2015302590161','180010',"245015259@qq.com")
    howard.get_token()
    cs.get_token()

    howard.stop_cancel()
    reservate_result_hw,location_hw = howard.reservate(roomId,seat_no,str(today),start,end)
    if reservate_result_hw == False:
        howard.loop_reservate()
    cs.stop_cancel()
    reservate_result_cs,location_cs = cs.reservate(roomId,seat_no+10,str(today),start,end)
    if reservate_result_cs == False:
        cs.loop_reservate()

 
    

def test():
    today = datetime.date.today()
    cs = user.User('2015302590161','180010',"245015259@qq.com")
    cs.get_token()
    reservate_result_cs,location_cs = cs.reservate(7,54,str(today),14.5,17)
    if reservate_result_cs == False:
        cs.loop_reservate()

    # howard.stop_cancel()
    # howard.reservate(7,29,str(today),12,13.5)


if __name__ == '__main__':

    if len(sys.argv) == 3:
        start = float(sys.argv[1])
        end = float(sys.argv[2])
        change_time(start=start,end=end)
    else:
        change_time()








