import requests
import lib
import os
import datetime
import util
import time



class User(object):
    def __init__(self,username='2015301020142',password='17871X',mail = None):
        self.__username = username
        self.__password = password
        self.__token = None
        self.__count = 0
        self.__mail = mail

    def get_username(self):
        return self.__username

    def rtn_token(self):
        return self.__token

    def count(self):
        if self.__count >= 6:
            self.__count = 0
            print('system overloading,process terminated')
            os._exit()
        ++self.__count

    #no return
    def get_token(self):
        login_url = 'https://seat.lib.whu.edu.cn:8443/rest/auth'
        data = {
            'username': self.__username,
            'password': self.__password
        }
        headers = {
            'Content-Tyep': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'seat.lib.whu.edu.cn:8443',
            'Connection': 'Connection',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-TL00 Build/HUAWEINXT-TL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }

        try:
            response = requests.get(login_url, params=data, headers=headers,timeout=5)
        except requests.Timeout:
            print('time out,retrying...{}'.format(self.__count))
            self.get_token(self)
        except  requests.RequestException:
            print('error:',requests.RequestException)
        except requests.exceptions.RequestException:
            print('errot:',requests.exceptions.RequestException)
        if response.status_code == 200:
            # get token
            response_json = response.json()
            self.__token = response_json.get('data').get('token')
            print('token got:',self.__token)
        else:
            print('error when getting token:', response.status_code)

    def loop_reservate(self,roomId=7,seat_no=51,start=14.5,end=17):
    	today = datetime.date.today()
    	token = self.__token
    	library = lib.Lib()

    	self.reservate_exclude(roomId,str(today),start,end)

    	while True:
    		time.sleep(8)
    		seats = library.free_seats(token,roomId,str(today),start,end)
    		if len(seats) == 0:
    			print('retrying...')
    			continue
    		self.stop_cancel()
    		result,location = self.reservate(roomId,seat_no,str(today),start,end)
    		if result == True:
    			break





    #if success return True,location, else return false,None
    def reservate(self,roomId=7,seat_no=41,date=str(datetime.date.today()),start=9,end=22):
        token = self.__token

        library = lib.Lib()
        seats_json = library.free_seats(token, roomId, date, start, end)

        #若选中的房间在指定时间段内无可用座位，则结束程序
        if(len(seats_json) == 0):
            print('not available seats in the room selected,finish')
            return False,None

        form = {
            'startTime': int(start * 60),
            'endTime': int(end * 60),
            'seat': 0,
            'date': date,
        }

        headers = {
            'token': token,
            'Host': 'seat.lib.whu.edu.cn:8443',
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-TL00 Build/HUAWEINXT-TL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Content-Tyep': 'application/x-www-form-urlencoded;charset=UTF-8',
        }

        minus = 9999
        s_id = ''
        for i in seats_json:
            seat = seats_json.get(i)
            seat_id = seat['id']
            seat_name = seat['name']
            s = abs(int(seat_name) - int(seat_no))
            if s < minus:
                minus = s
                s_id = seat_id
            if int(seat_name) > int(seat_no):
                break

        form['seat'] = s_id
        url = 'https://seat.lib.whu.edu.cn:8443/rest/v2/freeBook'
        try:
            result = requests.post(url, data=form, headers=headers)
        except requests.Timeout:
            self.count()
            self.get_token()
            print('time out when reservating {}'.format(self.__count))
            self.reservate(self, roomId, seat_no, date, start, end)
        except requests.RequestException:
            print('error when reservating:',requests.RequestException)
        if result.status_code == 200:
            status = result.json().get('status')
            if status == 'success':
                location = result.json().get('data').get('location')
                print('预约成功:', location)
                if self.__mail != None:
                	util.Util.sendMail(self.__mail,location+'，时间'+str(start)+' -- '+str(end))
                return True,location
            else:
                print('预约失败:',result.json().get('message'))
        else:
            print('reservation_err:', result.status_code)

        return False,None
    #预约二楼西 二楼东 三楼西 三楼东 ，四楼西，四楼东，三楼自主学习区 任意一个座位
    def reservate_exclude(self,exclude_id,date,start,end):
        all_room_id = [6,7,8,10,9,11,12]
        for id in all_room_id:
            if id == exclude_id:
                continue
            result,location = self.reservate(id,'052',date,start,end)
            if result == True:
                return True,location
        return False,None


    #if using seat,return True,stat(RESERVE,CHEKE_IN,AWAY),id , else return False,None,None
    def reservation(self):
        token = self.__token
        url = 'https://seat.lib.whu.edu.cn:8443/rest/v2/history/1/10'
        headers = {
            'token': token,
            'Content-Tyep': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'seat.lib.whu.edu.cn:8443',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-TL00 Build/HUAWEINXT-TL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }
        try:
            response = requests.get(url=url,headers=headers,timeout=3)
        except  requests.Timeout:
            print('time out when getting reservation {},retrying...'.format(self.__count))
            self.get_token()
            self.count()
            return self.reservation()
        except  requests.RequestException:
            print('error when getting reservation :', requests.RequestException)
            return
        reservations = response.json().get('data').get('reservations')
        for r in reservations:
            if r.get('stat') == 'RESERVE' or r.get('stat') == 'CHECK_IN' or r.get('stat') == 'AWAY' :
                return True,r.get('stat'),str(r.get('id'))

        return False,None,None



    #id should be str,if success return True,else return False
    def cancel(self,id):

        token = self.__token
        url = 'https://seat.lib.whu.edu.cn:8443/rest/v2/cancel/'
        url = url + id
        headers = {
            'token':token,
            'Content-Tyep': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'seat.lib.whu.edu.cn:8443',
            'Connection': 'Connection',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-TL00 Build/HUAWEINXT-TL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }

        try:
            response = requests.get(url=url,headers=headers,timeout=5)
        except  requests.Timeout:
            print('time out when canceling,retrying...')
            return self.cancel(id)
        except  requests.RequestException:
            print('error when cancling:',requests.RequestException)
        status = response.json().get('status')
        if status == 'success':
            print('cancled')
            return True

        return False

    def stop(self):
        url = 'https://seat.lib.whu.edu.cn:8443/rest/v2/stop'
        headers = {
            'token': self.__token,
            'Content-Tyep': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'seat.lib.whu.edu.cn:8443',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-TL00 Build/HUAWEINXT-TL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }
        try:
            response = requests.get(url=url,headers=headers,timeout=5)
        except  requests.Timeout:
            print('time out when canceling,retrying...')
            return self.stop()
        except  requests.RequestException:
            print('error when cancling:',requests.RequestException)
        status = response.json().get('status')
        if status == 'success':
            print('cancled')
            return True

        return False

    def stop_cancel(self):
        b,status,id = self.reservation()
        #无正在使用的座位,return
        if b == False:
            return
        else:
            if status == 'RESERVE':
                self.cancel(id)
                return
            else:
                self.stop()






