import requests
import numpy as np
from bs4 import BeautifulSoup as bs

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import wget

def download(urls):
    
    home = 'https://www.nzgd.org.nz/(S(scnf1sdhnfocsffjm5zfl12v))/ARCGISMapViewer/mapviewer.aspx'
    link = 'https://www.nzgd.org.nz/(S(z0hp2wn5amri2plh1wj5sgpw))/GeotechnicalInvestigationDataEntry.aspx?popup=1#/Upload/Location/64/InvestigationLog/64'


    browser = webdriver.Chrome('/usr/local/bin/chromedriver') # Get local session of chrome


    c = browser.get(link)
    time.sleep(3)

    elem_user = browser.find_element_by_id("UserName")
    elem_user.send_keys("your email")
    elem_pwd = browser.find_element_by_id("Password")
    elem_pwd.send_keys("your password")
    login_url = browser.current_url
    # click login
    try:
        login_btn = browser.find_element_by_id("LoginButton").click()
    except:
        print("Login failed!\n")
    time.sleep(5)
    # check login status
    waittime = 5
    while browser.current_url == login_url:
        print('waiting another 1s to login...')
        time.sleep(1)
        waittime += 1
        if waittime == 10:
            print("too long to login, stoped.")
            exit()
    print('login maybe succeed...\n')


    # get cookies
    cookies = browser.get_cookies()
    cookie = [item["name"] + "=" + item["value"] for item in cookies]
    cookiestr = ';'.join(item for item in cookie)



    c = browser.get(home)
    linksList = 'pagelinks.txt'
    count=0.0
    all = len(urls)


    for line in urls:
        try:
            url = line.strip()
            print(url)
            c = browser.get(url)
            time.sleep(4)
            ags = browser.find_element_by_partial_link_text('_AGS01.xls')
            ags.click()
        except:
            print("one line skipped..")

        count += 1
        print(count/all*100.0)

    time.sleep(3)
    browser.close()




