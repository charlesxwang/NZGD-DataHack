# This is the main script used two identify cpt url from NZGD.
# Make sure you get authorization to download data from NZGD, you need username and password to login.
# Charles Wang
# updated Aug 02, 2017


import requests
import numpy as np
from bs4 import BeautifulSoup as bs

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import wget



home = 'https://www.nzgd.org.nz/(S(scnf1sdhnfocsffjm5zfl12v))/ARCGISMapViewer/mapviewer.aspx'
link = 'https://www.nzgd.org.nz/(S(z0hp2wn5amri2plh1wj5sgpw))/GeotechnicalInvestigationDataEntry.aspx?popup=1#/Upload/Location/64/InvestigationLog/64'


# configure the browser
browser = webdriver.Chrome('/usr/local/bin/chromedriver') # Get local session of chrome
c = browser.get(link)
time.sleep(3)
elem_user = browser.find_element_by_id("UserName")
elem_user.send_keys("your login email")           # email
elem_pwd = browser.find_element_by_id("Password")
elem_pwd.send_keys("your password")               # password
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
print('login maybe succeeded...\n')


# get cookies
cookies = browser.get_cookies()
cookie = [item["name"] + "=" + item["value"] for item in cookies]
cookiestr = ';'.join(item for item in cookie)

# go to the mapview
c = browser.get(home)
# now you can zoom the map to sellect your ROI and customize your data, then wait...
time.sleep(120)


# hide some elements in the mapview
b1 = browser.find_element_by_class_name('esriControlsBR')
b2 = browser.find_element_by_id('map_zoom_slider')
b3 = browser.find_element_by_id('mapLeftMenu')
b4 = browser.find_element_by_id('mapMenuContainer')
b5 = browser.find_element_by_class_name('esriScalebar')
browser.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", b1)
browser.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", b2)
browser.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", b3)
browser.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", b4)
browser.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", b5)

# find the handles of symbols, they are too large
container = browser.find_element_by_id('Investigation_Log_Location_layer')
images = container.find_elements_by_css_selector("image[width*='20']")
# reduce the sizes of symbols
for point in images:
    browser.execute_script("arguments[0].setAttribute('width','5');", point)
    browser.execute_script("arguments[0].setAttribute('height','5');", point)

# read urls from each symbols, each represents the page of a data point where investigation was made.
pop = browser.find_element_by_class_name('esriPopup')
pagelinks=[]
count=0.0
all=len(images)
for point in images:

    browser.execute_script("arguments[0].style.visibility='hidden';", pop)
    try:
        point.click()
        time.sleep(4)
        #browser.execute_script("arguments[0].style.visibility='visible';", pop)
        frame = browser.find_element_by_tag_name('iframe')
        pagelink = frame.get_attribute("src")
        pagelinks.append(pagelink.strip()+"\n")

    except:
        print("not clicked...")

    count += 1
    print(count/all*100.0)


# output urls
with open("pagelinks.txt", "w+") as fo:
    line = fo.writelines(pagelinks)




