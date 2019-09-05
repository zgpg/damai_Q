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
    round = get_config('model', 'round')
    quantity = get_config('model', 'quantity')
    grade = get_config('model', 'grade')
    url = get_config('model', 'url')
    
    os_name = platform.system().lower()
    if 'windows' == os_name:
        chromedriver = r"driver/chromedriver.exe"
    else:
        chromedriver = r"driver/chromedriver"
    driver = webdriver.Chrome(chromedriver)

    def login(self):
        #登陆

        self.driver.get('https://passport.damai.cn/login')

        WebDriverWait(self.driver, 3000).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-spm="duserinfo"]/div')))
        print('登陆成功')
        user_name = self.driver.find_element_by_xpath('//a[@data-spm="duserinfo"]/div').text
        print('账号：', user_name)
        self.driver.get(self.url)
        print('跳转抢票页面')

    def choose_tickets(self):
        #选择场次和票档
        print('选择场次')
        c_session = self.driver.find_element_by_xpath(f'//div[@class="perform__order__select perform__order__select__performs"]/div[2]/div[1]/div[{self.round}]/span[2]')
        c_session.click()
        time.sleep(0.1)
        print('选择票档')
        ticket_file = self.driver.find_element_by_xpath(f'//div[@class="perform__order__select perform__order__select__performs"]/following-sibling::div[2]/div[2]/div[1]/div[{self.grade}]')
        ticket_file.click()

        #判断购买几张票
        if int(self.quantity) > 1:
            try:
                print(self.quantity,"张票")
                ticket_input = self.driver.find_element_by_xpath('//input[@class="cafe-c-input-number-input"]')
                #ticket_input.click()
                ticket_input.clear()
                ticket_input.send_keys(self.quantity)
                #self.driver.find_element_by_xpath('//a[@class="cafe-c-input-number-handler cafe-c-input-number-handler-up"]').click()
            except Exception as e:
                print("未成功点击+号", e)

    def detail_page_auto(self):
        
        while self.driver.title != '确认订单':
            dbuy_button = self.driver.find_element_by_xpath('//div[@data-spm="dbuy"]')
            print('寻找按钮:', dbuy_button.text)
            print("---开始进行日期及票价选择---")
            try:
                if dbuy_button.text == "即将开售":
                    print('---抢票未开始，等待刷新开始---')
                    continue

                elif dbuy_button.text == "开售提醒":
                    print('还不到抢票时间，开售提醒')
                    break

                elif dbuy_button.text == "立即预定":
                    self.choose_tickets()
                    dbuy_button.click()

                elif dbuy_button.text == "立即预订":
                    self.choose_tickets()
                    #break
                    dbuy_button.click()

                elif dbuy_button.text == "立即购买":
                    self.choose_tickets()
                    dbuy_button.click()

                elif dbuy_button.text == "提交缺货登记":
                    print('---抢票失败，请手动提交缺货登记---')  
                    break

                else:
                    dbuy_button.click()

            except Exception as ex:
                print('---未跳转到订单结算界面---',ex)
                
    def confirm_auto(self):
        #确认订单

        print('开始确认订单')
        title = self.driver.title
        while title != '确认订单':
            title = self.driver.title
        
        print('开始选择购票人',self.quantity)
        try:
            #2个票需要选择2个身份证
            self.driver.find_element_by_xpath(
                '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div/label/span[1]/input').click()
            self.driver.find_element_by_xpath(
                '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div[2]/label/span[1]/input').click()
        except Exception as e:
            print('购票人选择出错', e)

        print('success')
        self.driver.find_element_by_xpath('//div[@class="submit-wrapper"]/button').click()


if __name__ == '__main__':
    print('版本1.1')

    myapp = App()
    myapp.login()
    myapp.detail_page_auto()
    myapp.confirm_auto()
