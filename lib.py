import requests

class Lib:

    #return free seats as json
    def free_seats(self,token,roomId,date,start,end):
        url = 'https://seat.lib.whu.edu.cn:8443/rest/v2/searchSeats'
        search_url = url + '/' + date + '/' + str(int(start*60)) + '/' + str(int(end * 60))
        headers = {
            'token': token,
            'Host': 'seat.lib.whu.edu.cn:8443',
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
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
                return r_json
            else:
                print('free_seat_json:', response.status_code, response.url)
                return None
        except requests.RequestException:
            print('error when get free seats:',requests.RequestException)