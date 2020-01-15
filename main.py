from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
import time
import os
import platform

config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')


def get_config(section, key):
    return config.get(section, key)


class App:
    #dotakey = get_config('info', 'privilege_val')
    name = get_config('info', 'name')
    phone = get_config('info', 'phone')
    grade = get_config('model', 'grade')
    url = get_config('model', 'url')
    status = 0#状态,表示如今进行到何种程度
    num = 0
    
    os_name = platform.system().lower()
    if 'windows' == os_name:
        chromedriver = r"driver/chromedriver.exe"
    else:
        chromedriver = r"driver/chromedriver"
    driver = webdriver.Chrome(chromedriver)

    def login(self):
        #登陆
        self.driver.get('https://passport.damai.cn/login')

        WebDriverWait(self.driver, 3000).until(EC.presence_of_element_located((By.XPATH, '//a[@data-spm="duserinfo"]/div')))
        print('登陆成功')
        self.status = 1
        user_name = self.driver.find_element_by_xpath('//a[@data-spm="duserinfo"]/div').text
        print('账号：', user_name)
        self.driver.get(self.url)
        print('跳转抢票页面')
        self.status = 2


    def detail_page_auto(self):
        if(self.status == 2):
        
            self.num=1#第一次尝试
            time_start=time.time()

            while self.driver.title != '确认订单':
                if self.num!=1:#如果前一次失败了，那就刷新界面重新开始
                    self.status=2
                    print(self.num,"次失败，重新选择")
                    self.driver.get(self.url)

                try:    
                    element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="perform__order__select perform__order__select__performs"]/following-sibling::div[2]/div[2]/div[1]')))
                except Exception as e:
                    print(e)
                pricelist=element.find_elements_by_xpath('div')
                print("开始选择票档")
                gradeList = self.grade.split(',')
                gradeNum = 0
                for i in gradeList:
                    gradeNum+=1
                    print(i,pricelist[int(i)-1].text)
                    ishave = App.isElementExist(pricelist[int(i)-1],'span')
                    if ishave:
                        continue
                    else:
                        print("有可以选择的票档了"+pricelist[int(i)-1].text)
                        pricelist[int(i)-1].click()
                        break
                #print(gradeNum,len(gradeList))
                if(gradeNum == len(gradeList)):
                    self.num+=1
                    print("都没有票了，我再刷新页面试一下")
                    print(self.num,"次失败，重新选择")
                    self.driver.get(self.url)
                dbuy_button = self.driver.find_element_by_xpath('//div[@data-spm="dbuy"]')
                print('寻找按钮:', dbuy_button.text)
                print("---开始进行日期及票价选择---")
                try:
                    if dbuy_button.text == "即将开抢":
                        print('---抢票未开始，等待刷新开始---')
                        continue

                    elif dbuy_button.text == "即将开售":
                        print('---抢票未开始，等待刷新开始---')
                        continue

                    elif dbuy_button.text == "开售提醒":
                        print('还不到抢票时间，开售提醒')
                        break
                    elif dbuy_button.text == "立即预定":
                        self.status = 3
                        dbuy_button.click()

                    elif dbuy_button.text == "立即预订":
                        self.status = 3
                        dbuy_button.click()

                    elif dbuy_button.text == "立即购买":
                        self.status = 3
                        dbuy_button.click()
                    elif dbuy_button.text == "提交缺货登记":
                        self.num+=1
                        print("都没有票了，我再刷新页面试一下")
                        print(self.num,"次失败，重新选择")
                        self.driver.get(self.url)
                    else:
                        dbuy_button.click()

                except Exception as ex:
                    print('---未跳转到订单结算界面---',ex)
                self.num+=1
    def confirm_auto(self):
        #确认订单
        if(self.status == 3):
            print('开始确认订单')
            title = self.driver.title
            while title != '确认订单':
                title = self.driver.title

            print('开始选择购票人')                  
            try:    
            #2个票需要选择2个身份证               
                self.driver.find_element_by_xpath(
                    '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div/label/span[1]/input').click() 
              
            except Exception as e: 
                print('购票人选择出错', e)
                self.driver.get(self.url)
            
            print('success')
            #self.driver.find_element_by_xpath('//div[@class="submit-wrapper"]/button').click()
    def isElementExist(browser,element):
        flag=True
        try:
            browser.find_element_by_xpath(element)
            return flag
        except:
            flag=False
            return flag

if __name__ == '__main__':
    print('版本1.4')

    now = int(time.time())
    go_time = get_config('model', 'date')
    timeArray = time.strptime(go_time, "%Y-%m-%d %H:%M:%S")
    go_timeint = int(time.mktime(timeArray))
    time_left = go_timeint-now
    myapp = App()
    myapp.login()
    while time_left > 0:
        print('倒计时(s):',time_left)
        time.sleep(1)
        time_left = time_left - 1
        if(time_left == 12):
            print("开始执行抢票程序")
            myapp.detail_page_auto()
            myapp.confirm_auto()
            break
    else:
        myapp.detail_page_auto()
        myapp.confirm_auto()
        print('done!')
