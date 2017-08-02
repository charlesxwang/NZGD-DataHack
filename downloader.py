# Charles Wang
# updated Aug 02, 2017

import requests
import numpy as np
from bs4 import BeautifulSoup as bs

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from multiprocessing.dummy import Pool as ThreadPool
from selenium.webdriver.common.keys import Keys
import time
import wget


from downlib import download


linksList = 'pagelinks.txt'
urls = []
with open(linksList, "r") as file:
    for line in file:
        try:
            url = line.strip()
            if url:
                urls.append(url)
        except:
            print("no url in this lind...\n")

ncpu = 8
step = int(len(urls)/ncpu)+1
chunks = [urls[x:x+step] for x in xrange(0, len(urls), step)]

# get some workers
pool = ThreadPool(ncpu)
# send job to workers, make sure to give them food.
# no food no work.
results = pool.map(download, chunks)
# jobs are done, clean the site
pool.close()
pool.join()


