from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from time import sleep
import os
from homepage.models import CPU,GPU,MEM,STORAGE,PWR,CASE,MOBO,FAN
from math import floor
redir = ['https://pcpartpicker.com/products/cpu/','https://pcpartpicker.com/products/video-card/#c=476,439,450,438,436,446,425,447,427,448,424,392,391,431,445,444&page=1&sort=chipset','https://pcpartpicker.com/products/memory/#U=4&Z=8192002,16384002,32768002&t=14&S=3000,3866&page=1&sort=price','https://pcpartpicker.com/products/internal-hard-drive/#page=1','https://pcpartpicker.com/products/power-supply/#e=6,5,4,3,2&page=1&sort=price','https://pcpartpicker.com/products/case/#t=4,3','https://pcpartpicker.com/products/motherboard/#f=2&L=4&page=1&sort=price','https://pcpartpicker.com/products/cpu-cooler/']
def importCPU(browser):
    menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
    sleep(.5)
    items = menu.find_elements_by_tag_name('tr')
    full = CPU.objects.all()
    full.update(last_updated=None)
    for item in items:
        section = item.find_elements_by_tag_name('td')
        price = section[9].text
        price = price.replace('Add','')
        price = price[1:]
        links = section[9].find_element_by_tag_name('button').get_attribute('data-product-tag')
        temp = full.filter(links=links)
        if price == '':
            temp.update(price=None)
        else:
            temp.update(price=price)
def importGPU(browser):
    sleep(.5)
    pages = browser.find_element_by_css_selector('.pagination').find_elements_by_tag_name('li')
    pagesNo = int(pages[-1].text)
    full = GPU.objects.all()
    full.update(last_updated=None)
    for i in range(1,pagesNo+1):
        menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
        sleep(.5)
        items = menu.find_elements_by_tag_name('tr')
        for item in items:
            section = item.find_elements_by_tag_name('td')
            price = section[9].text
            price = price.replace('Add','')
            price = price[1:]
            links = section[9].find_element_by_tag_name('button').get_attribute('data-product-tag')
            temp = full.filter(links=links)
            if price == '':
                temp.update(price=None)
            else:
                temp.update(price=price)
        if i != pagesNo:
            browser.find_element_by_css_selector('.pagination').find_element_by_link_text(str(i+1)).click()
def importMEM(browser):
    sleep(.5)
    MEM.objects.all().update(last_updated=None)
    for i in range(1,6):
        menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
        sleep(.5)
        items = menu.find_elements_by_tag_name('tr')
        for item in items:
            section = item.find_elements_by_tag_name('td')
            if section[9].text[0]=='$':
                name = section[1].text
                modules = name[-5:]
                speed = section[2].text
                speed = speed[-4:]
                cas = section[7].text
                price = section[9].text
                price = price.replace('Add','')
                price = price[1:]
                color = section[5].text
                realspeed = section[6].text
                realspeed = float(realspeed.replace(' ns',''))
                links = section[9].find_element_by_tag_name('button').get_attribute('data-product-tag')
                img = section[1].find_element_by_tag_name('a').find_element_by_tag_name('div').find_element_by_tag_name('div').find_element_by_tag_name('img').get_attribute('src')
                speedperdollar = round(1/(price*realspeed)*10000)
                temp = MEM.objects.all().filter(links=links)
                if temp:
                    temp.update(price=price)
                    temp.update(speedperdollar=speedperdollar)
                else:
                    mem = MEM(name=name,speed=speed,cas=cas,modules=modules,price=price,links=links,img=img,color=color,realspeed=realspeed,speedperdollar=speedperdollar)
                    mem.save()
        if i != 5:
            browser.find_element_by_css_selector('.pagination').find_element_by_link_text(str(i+1)).click()
def importSTORAGE(browser):
    browser.get('https://pcpartpicker.com/products/internal-hard-drive/#page=1')
    sleep(.5)
    STORAGE.objects.all().update(last_updated=None)
    for i in range(1,5):
        menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
        sleep(.5)
        items = menu.find_elements_by_tag_name('tr')
        for item in items:
            section = item.find_elements_by_tag_name('td')
            if section[9].text[0]=='$': # price has id we can search later
                name = section[1].text
                capacityst = section[2].text
                if capacityst[-2:] == 'TB':
                    capacity = floor(float(capacityst[:capacityst.find(' ')])*1000)
                else:
                    capacity = int(capacityst[:capacityst.find(' ')])
                kind = section[4].text
                form = section[7].text
                price = section[9].text
                price = price.replace('Add','')
                price = price[1:]
                links = section[9].find_element_by_tag_name('button').get_attribute('data-product-tag')
                img = section[1].find_element_by_tag_name('a').find_element_by_tag_name('div').find_element_by_tag_name('div').find_element_by_tag_name('img').get_attribute('src')
                temp = STORAGE.objects.all().filter(links=links)
                if temp:
                    temp.update(price=price)
                else:
                    storage = STORAGE(name=name,capacity=capacity,price=price,form=form,kind=kind,links=links,img=img)
                    storage.save()
        if i != 4:
            browser.find_element_by_css_selector('.pagination').find_element_by_link_text(str(i+1)).click()
def importPWR(browser):
    browser.get('https://pcpartpicker.com/products/power-supply/#e=6,5,4,3,2&page=1&sort=price')
    sleep(.5)
    PWR.objects.all().update(last_updated=None)
    for i in range(1,3):
        menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
        sleep(.5)
        items = menu.find_elements_by_tag_name('tr')
        for item in items:
            section = item.find_elements_by_tag_name('td')
            if section[8].text[0]=='$': # price has id we can search later
                name = section[1].text
                rating = section[3].text
                wattage = section[4].text
                wattage = wattage[:-2]
                price = section[8].text
                price = price.replace('Add','')
                price = price[1:]
                img = section[1].find_element_by_tag_name('a').find_element_by_tag_name('div').find_element_by_tag_name('div').find_element_by_tag_name('img').get_attribute('src')
                links = section[8].find_element_by_tag_name('button').get_attribute('data-product-tag')
                temp = PWR.objects.all().filter(links=links)
                if temp:
                    temp.update(price=price)
                else:
                    pwr = PWR(name=name,wattage=wattage,price=price,rating=rating,links=links,img=img)
                    pwr.save()
        if i != 2:
            browser.find_element_by_css_selector('.pagination').find_element_by_link_text(str(i+1)).click()
def importCASE(browser):
    browser.get('https://pcpartpicker.com/products/case/#t=4,3')
    menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
    sleep(.5)
    items = menu.find_elements_by_tag_name('tr')
    full = CASE.objects.all()
    full.update(last_updated=None)
    for item in items:
        section = item.find_elements_by_tag_name('td')
        price = section[9].text
        price = price.replace('Add','')
        price = price[1:]
        links = section[9].find_element_by_tag_name('button').get_attribute('data-product-tag')
        temp = full.filter(links=links)
        if price == '':
            temp.update(price=None)
        else:
            temp.update(price=price)
def importMOBO(browser):
    browser.get('https://pcpartpicker.com/products/motherboard/#f=2&L=4&page=1&sort=price')
    menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
    sleep(.5)
    items = menu.find_elements_by_tag_name('tr')
    MOBO.objects.all().update(last_updated=None)
    for item in items:
        section = item.find_elements_by_tag_name('td')
        if section[8].text[0]=='$': # price has id we can search later
            name = section[1].text
            chipset = section[2].text
            price = section[8].text
            price = price.replace('Add','')
            price = price[1:]
            links = section[8].find_element_by_tag_name('button').get_attribute('data-product-tag')
            img = section[1].find_element_by_tag_name('a').find_element_by_tag_name('div').find_element_by_tag_name('div').find_element_by_tag_name('img').get_attribute('src')
            temp = MOBO.objects.all().filter(links=links)
            if temp:
                temp.update(price=price)
            else:
                mobo = MOBO(name=name,price=price,chipset=chipset,links=links,img=img)
                mobo.save()
def importFAN(browser):
    browser.get('https://pcpartpicker.com/products/cpu-cooler/')
    menu = WebDriverWait(browser,1).until(presence_of_element_located((By.CSS_SELECTOR,'#category_content')))
    sleep(.5)
    items = menu.find_elements_by_tag_name('tr')
    full = FAN.objects.all()
    full.update(last_updated=None)
    for item in items:
        section = item.find_elements_by_tag_name('td')
        price = section[7].text
        price = price.replace('Add','')
        price = price[1:]
        links = section[7].find_element_by_tag_name('button').get_attribute('data-product-tag')
        temp = full.filter(links=links)
        if price == '':
            temp.update(price=None)
        else:
            temp.update(price=price)
path = os.getcwd()+'\\geckodriver.exe'
browser=webdriver.Firefox(executable_path=path)
browser.get(redir[0])
importCPU(browser)
browser.get(redir[1])
importGPU(browser)
browser.get(redir[2])
importMEM(browser)
browser.get(redir[3])
importSTORAGE(browser)
browser.get(redir[4])
importPWR(browser)
browser.get(redir[5])
importCASE(browser)
browser.get(redir[6])
importMOBO(browser)
browser.get(redir[7])
importFAN(browser)
browser.close()