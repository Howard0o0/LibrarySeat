import requests
import os

class Lib:

    def __init__(self):
        self.__count = 0

    def count(self):
        if self.__count >= 6:
            self.__count = 0
            print('system overloading,process terminated')
            os._exit()
        ++self.__count

    #return free seats as json
    def free_seats(self,token,roomId,date,start,end):
        url = 'https://seat.lib.whu.edu.cn:8443/rest/v2/searchSeats'
        search_url = url + '/' + date + '/' + str(int(start*60)) + '/' + str(int(end * 60))
        headers = {
            'token': token,
            'Host': 'seat.lib.whu.edu.cn:8443',
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-TL00 Build/HUAWEINXT-TL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }

        form = {
            '"t': 1,
            'roomId': roomId,
            'buildingId': 1,
            'batch': 9999,
            'page': 1,
            't2': '2"'
        }

        try:
            response = requests.post(search_url, data=form, headers=headers)
            if response.status_code == 200:
                r_json = response.json()
                # print(r_json)
                return r_json.get('data').get('seats')
            else:
                print('free_seat_json:', response.status_code, response.url)
                self.count()
                return self.free_seats(token,roomId,date,start,end)
        except requests.RequestException:
            print('error when get free seats:',requests.RequestException)