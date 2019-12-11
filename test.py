from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
import time
import os
import platform
import datetime

config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')


def get_config(section, key):
    return config.get(section, key)


        
if __name__ == '__main__':
    print('版本1.0')

    now = int(time.time())
    go_time = get_config('model', 'date')
    timeArray = time.strptime(go_time, "%Y-%m-%d %H:%M:%S")
    
    go_timeint = int(time.mktime(timeArray))
    print(go_timeint)
    exit()
    time_left = go_timeint-now
