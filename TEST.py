import webbrowser
# pip install selenium
# pip install requests
# pip install fake_useragent
# 預設瀏覽器
#a=webbrowser.get('windows-default')
#a.open('https://www.python.org/downloads/windows/')
# 使用新視窗、Tab開啟頁面
#a.open_new('https://www.google.com')
#a.open_new_tab('https://www.google.com')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os,time
import requests
from fake_useragent import UserAgent
#程式中斷點用
#import sys
#sys.exit()

ua = UserAgent()
user_agent = ua.random

#nochoosetype = int(input('請輸入預設執行大禮包(1.YES CHROME/2.YES FF/3.NO)：輸入數字\n'))
nochoosetype = 4

#設定執行組合
if nochoosetype == 1:
    drivertype = 1
    folderpathtype = 1
    cmdtype = 2
elif nochoosetype == 2:
    drivertype = 2
    folderpathtype = 1
    cmdtype = 2
elif nochoosetype == 4:#TESTMODE
    drivertype = 1
    folderpathtype = 1
    cmdtype = 1
else:
    drivertype = int(input('請輸入執行瀏覽器種類(1.Chrome/2.FireFox)：輸入數字\n'))
    folderpathtype = int(input('請輸入截圖存檔位置(1.C:/CheckMeCheckMe /2.C:/TempPic)：輸入數字\n'))
    cmdtype = int(input('請輸入CMD URL選擇(1.CMDBET /2.CMD558)：輸入數字\n'))
    #drivertype = 1
    #folderpathtype = 1
    #cmdtype = 2

#執行瀏覽器
if drivertype == 2:
    ###https://github.com/mozilla/geckodriver/releases
    driver = webdriver.Firefox()
    options = webdriver.FirefoxOptions()
    user_agent = ua.firefox
else:
    ###https://sites.google.com/chromium.org/driver/downloads
    driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    user_agent = ua.google 
    #driver.get('https://www.python.org/downloads/windows/')

#selenium被識別自動化，修改navigator
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

#圖片儲存路徑
if folderpathtype == 1:
    #儲存圖片檔案路徑    
    folderpath = 'C:/CheckMeCheckMe'
else:
    folderpath = 'C:/TempPic'

#圖片檔案名稱使用時間戳記命名
current_time1 = time.strftime("%Y-%m-%d", time.localtime(time.time()))

#主要執行模組
def openWebSite(GetList,Checkstr):
    #拆輸入清單
    for WebName in GetList:
        for index in range(len(WebName)):
            webweb = WebName[index-1]
            if index == 1:
                pic_path = folderpath + '/' + webweb + '_' + current_time1 + '.png'
                pageshow = driver.get(WebName[index])
                con = driver.find_element_by_tag_name('html').text
                CheckWebFin = con.find(Checkstr)
                #網頁header隨機UA
                if drivertype == 2:
                    user_agent = ua.firefox
                else:
                    user_agent = ua.google
                headers = {'User-agent': user_agent}
                rBackCode = requests.get(WebName[index],headers=headers)
                
                try:
                    os.makedirs(folderpath)
                # 檔案已存在的例外處理
                except FileExistsError:
                    True
                except PermissionError:
                    print("權限不足。")
                driver.save_screenshot(pic_path)

                if rBackCode.status_code == requests.codes.ok:
                    if CheckWebFin >= 0:
                        print(webweb,"OK")
                        #print(WebName[index],Checkstr,webweb)
                    else:
                        print(webweb,"Not")
                else:
                    print(webweb,"ERROR_CODE：",rBackCode.status_code,rBackCode.reason)

#原 http://www.cmdbet.com 
#換成 http://www.cmd558.com/
if cmdtype == 1:
    checklist = [('CMD368','http://www.cmdbet.com')
    ,('mobile_CMD368','http://mobile.cmdbet.com')
    ,('3in1bet','http://www.3in1bet.com')
    ,('mobile_3in1bet','http://mobile.3in1bet.com')
    ,('Max222','http://www.max222.com')
    ,('mobile_Max222','http://mobile.max222.com')
    ,('Cbet','http://www.cbetus.com')
    ,('mobile_Cbet','http://mobile.cbetus.com')]
else:
    checklist = [('CMD368','http://www.cmd558.net')
    ,('mobile_CMD368','http://mobile.cmdbet.com')
    ,('3in1bet','http://www.3in1bet.com')
    ,('mobile_3in1bet','http://mobile.3in1bet.com')
    ,('Max222','http://www.max222.com')
    ,('mobile_Max222','http://mobile.max222.com')
    ,('Cbet','http://www.cbetus.com')
    ,('mobile_Cbet','http://mobile.cbetus.com')]

Api_checklist = [('API_BO','http://bo.flashtechsolution.com/')]
Api_checklist2 = [('API','http://www.flashtechsolution.net')]
CheckHtmlStr = 'Our website is currently under maintenance'
Api_CheckHtmlStr = 'Our website is currently under maintenance'
Api_CheckHtmlStr2 = ''

#checklist = [('CMD368','http://www.cmdfx.com'),('mobile_CMD368','http://mobile.cmdbet.com')]
openWebSite(checklist,CheckHtmlStr)
openWebSite(Api_checklist,Api_CheckHtmlStr)
openWebSite(Api_checklist2,Api_CheckHtmlStr2)
#openWebSite_neibu()

driver.quit()
input('\n確認結果')
#pyinstaller -F CheckCheck.py