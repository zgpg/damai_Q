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
    express = get_config('model', 'express')
    grade = get_config('model', 'grade')
    url = get_config('model', 'url')
    
    os_name = platform.system().lower()
    if 'windows' == os_name:
        chromedriver = r"driver/chromedriver.exe"
    else:
        chromedriver = r"driver/chromedriver"
    driver = webdriver.Chrome(chromedriver)

    def login(self):
        """登陆模块"""

        self.driver.get('https://passport.damai.cn/login')

        WebDriverWait(self.driver, 3000).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-spm="duserinfo"]/div')))
        print('登陆成功')
        user_name = self.driver.find_element_by_xpath('//a[@data-spm="duserinfo"]/div').text
        print('账号：', user_name)

    def detail_page_auto(self):
        """详情页自动"""

        print('跳转页面')
        self.driver.get(self.url)
        #self.driver.get('https://detail.damai.cn/item.htm?pos=1&acm=201808136-1.1003.2.6372738&id=599841530617&scm=1003.2.201808136-1.OTHER_1566475770322_6372738?spm=a2oeg.home.banner.ditem_0.5b4223e1bf2zHd&clicktitle=%E6%AD%A6%E6%B1%89%E5%BC%A0%E9%9F%B6%E6%B6%B5')
        print('选择场次')
        self.driver.find_element_by_xpath(f'//div[@class="perform__order__select perform__order__select__performs"]/div[2]/div[1]/div[{self.round}]/span[2]').click()
        time.sleep(0.2)
        print('选择票档')
        self.driver.find_element_by_xpath(f'//div[@class="perform__order__select perform__order__select__performs"]/following-sibling::div[2]/div[2]/div[1]/div[{self.grade}]').click()
        dbuy_button = self.driver.find_element_by_xpath('//div[@data-spm="dbuy"]')
        #判断购买几张票
        if int(self.quantity) > 1:
            try:
                self.driver.find_element_by_xpath(
                    '//a[@class="cafe-c-input-number-handler cafe-c-input-number-handler-up"]').click()
            except Exception as e:
                print("未成功点击+号", e)
        print('寻找按钮:', dbuy_button.text)
        print("###开始进行日期及票价选择###")
        while self.driver.title != '确认订单':
            try:
                if dbuy_button.text == "即将开抢":
                    print('###抢票未开始，刷新等待开始###')
                    continue

                elif dbuy_button.text == "提交开售提醒":
                    print('###提交开售提醒###')
                    break
                elif dbuy_button.text == "立即预定":
                    dbuy_button.click()

                elif dbuy_button.text == "立即预订":
                    dbuy_button.click()

                elif dbuy_button.text == "立即购买":
                    dbuy_button.click()

                elif dbuy_button.text == "提交缺货登记":
                    print('###抢票失败，请手动提交缺货登记###')  
                    break

            except:
                print('###未跳转到订单结算界面###')
                
    def confirm_auto(self):
        """自动确认订单"""

        title = self.driver.title
        while title != '确认订单':
            title = self.driver.title
        if self.express == 'True':
            try:
                self.driver.find_element_by_xpath('//*[@id="confirmOrder_1"]/div[1]/div[2]/div[2]').click()
                time.sleep(2)
            except Exception as e:
                print('未能成功选择快递', e)

        else:
            try:
                self.driver.find_element_by_xpath(
                    '//div[@id="confirmOrder_1"]/div[1]/div[4]/div[1]/div[2]/span/input').send_keys(self.name)
                self.driver.find_element_by_xpath(
                    '//div[@id="confirmOrder_1"]/div[1]/div[4]/div[2]/div[2]/span[2]/input').send_keys(self.phone)
            except Exception as e:
                print('联系人输入出错', e)

        try:
            #2个票需要选择2个身份证
            self.driver.find_element_by_xpath(
                '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div/label/span[1]/input').click()
            self.driver.find_element_by_xpath(
                '//*[@id="confirmOrder_1"]/div[2]/div[2]/div[1]/div[2]/label/span[1]/input').click()
        except Exception as e:
            print('购票人选择出错', e)

        self.driver.find_element_by_xpath('//div[@class="submit-wrapper"]/button').click()


if __name__ == '__main__':
    print('版本1.0')

    myapp = App()
    myapp.login()
    myapp.detail_page_auto()
    myapp.confirm_auto()
