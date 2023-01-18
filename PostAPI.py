import requests
from SQLQuery import SQLQuery
from time import sleep
# 執行環境,1.DEV 2.UAT
run_environment = 2

class PostAPI:
    def __init__(self):
        if run_environment == 1:
            # 原測試環境(RD開發環境，DEV)
            self.url = "https://irentcar-app-test.azurefd.net"
        elif run_environment == 2:
            # UAT
            self.url = "https://irentcar-app-uat.azurefd.net"
        else:
            self.url = "https://irentcar-app-test.azurefd.net"
        

    def __auth_token(self, access_token, api, **data):
        url_api = self.url + api
        headers = {'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json'}
        # data要設定成參數
        # data = {"IDNO": id}
        response = requests.post(url_api, headers=headers, json=data)
        data = response.json()
        return data

    def wallet_return(self):
        '''
            Examples:

            | APIKeywords.Wallet Return | # 預定汽機車後，退還預授權金額
        '''
        api = "/api/WalletReturnJob"
        url = self.url + api
        response = requests.post(url)
        data = response.json()
        if data['ErrorMessage'] == "Success":
            print("Success")
            return data['ErrorMessage']

    def lates_person_notice(self, id):
        access_token = SQLQuery().get_access_token(id)
        api = "/api/PersonNotice"
        data = PostAPI().__auth_token(access_token, api)
        notification_id = data["Data"]["PersonNoticeObj"][0]["NotificationID"]
        read_flg = data["Data"]["PersonNoticeObj"][0]["readFlg"]
        # print(notification_id, read_flg)
        return access_token, notification_id, read_flg
    
    def read_person_notice(self, id):
        access_token, notice_id, read_flg = PostAPI().lates_person_notice(id)
        sleep(10)
        # 1:已讀, 0:未讀
        for i in range(10):  
            if read_flg == 0:
                api = "/api/PersonNoticeRead"
                data = PostAPI().__auth_token(access_token, api, NotificationID=notice_id)
                print("次數"+ str(i))
                if data["Result"] == '1':
                    return data
                    break
                else:
                    raise False
            else:
                break

    def donate(self, id):
        access_token = SQLQuery().get_access_token(id)
        api = "/api/WalletTransferStoredValue"
        data = PostAPI().__auth_token(access_token, api, IDNO="S157297495", Amount=20)
        print(data)

    def credit_auth(self, id):
        access_token = SQLQuery().get_access_token(id)
        api = "/api/CreditAuthJobV2/"
        data = PostAPI().__auth_token(access_token, api, GateNo=0, isRetry=0)
        print(data['Result'])

    def get_pre_credit_auth(self, id):
        # 預約排程需要先打這隻API
        access_token = SQLQuery().get_access_token(id)
        api = "/api/GetPreCreditAuthJob"
        data = PostAPI().__auth_token(access_token, api, Nday=2, NHour=6, FirstReserveTime=20,
        AuthGateCount=1, ReservationAuthGateCount=1, PrepaidDays=1)
        print(data) 
    
    def wallet_stored_by_credit(self, id, save_money):
        # 用信用卡儲值錢包
        access_token = SQLQuery().get_access_token(id)
        api = "/api/WalletStoredByCredit/"
        data = PostAPI().__auth_token(access_token, api, StoreMoney=save_money, StoreType=0)
        print(data)
        if data['Result'] == '1':
            return data
        else:
            raise Exception("儲值失敗")
           
# 改ID並自行輸入金額
# ID須已登入APP
# python .\PostAPI.py
if  __name__ == "__main__":
    test = PostAPI()
    # id = "S157297495"
    id = "L125548207"
    test.wallet_stored_by_credit(id, 10)
    # test.wallet_return()
    



