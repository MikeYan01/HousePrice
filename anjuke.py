# -*- coding: utf-8 -*-
import requests, sys
from bs4 import BeautifulSoup
import os
import pandas as pd
import datetime
import math
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

# How many pages one city has
def getNumPages(soup):
    raw_num = soup.find('div', attrs={"class" : "list-results"}).find('span', attrs={"class" : "result"}).find('em').get_text()
    return float(raw_num) * 1.0/60

# House's lounge and living rooms
def getRoomsLivings(text):
    result = []
    searchObj = re.search(r'(.?)室(.?)厅', text)
    result.append(searchObj.group(0)[0])
    result.append(searchObj.group(0)[2])
    return result

# House's area
def getArea(text):
    begin = 0
    end = 0
    for i in range(0, len(text)):
        if text[i] == '约':
            begin = i
        elif text[i] == '㎡':
            end = i
    return text[begin+1:end]

# House's orientation
def getOrientation(text):
    result = ''
    for i in range(0, len(text)):
        if text[i] == '南':
            result += 'S|'
        if text[i] == '东':
            result += 'E|'
        if text[i] == '北':
            result += 'N|'
        if text[i] == '西':
            result += 'W|'
    return result[:-1]

# House's price
def getPrice(text, area):
    searchObj = re.search(r'[0-9]+', text)
    totalPrice = int(searchObj.group(0)) * 10000
    unitPrice = math.ceil(totalPrice * 1.0 / float(area))
    result = []
    result.append(str(totalPrice))
    result.append(str(unitPrice))
    return result


if __name__=='__main__':
    all_city = pd.read_csv('Data/city.csv', encoding = 'utf-8')
    for index, row in all_city.iterrows():

        result = pd.DataFrame(columns=('communityName', 'rooms', 'livings', 'area', 'orientation', 'levelType', 'floors', 'source', 'unitPrice', 'totalPrice', 'transDate', 'city', 'div', 'street', 'url', 'detailed_url', 'ref_price', 'ref_unit'))

        # current city
        city_name = row['city_name']
        city_code = row['city_code']
        city_province = row['city_province']
        print(city_name)
        
        # Store result 
        if os.path.exists('Data/normalized/' + city_province + '/'):
            pass
        else:
            os.makedirs('Data/normalized/' + city_province + '/')

        # Starting page
        start = "https://{}.fang.anjuke.com/loupan/all/p1/".format(city_code)
        r = requests.get(start, headers = headers)
        pageStr = r.content
        soup = BeautifulSoup(pageStr, "html.parser", from_encoding="gbk")
        
        # Every page's content
        numPages = math.ceil(getNumPages(soup))
        for i in range(1, numPages+1):
            if i != 1:
                theHref = "https://{}.fang.anjuke.com/loupan/all/p{}/".format(city_code, i)
                r = requests.get(theHref, headers = headers)
                pageStr = r.content
                soup = BeautifulSoup(pageStr, "html.parser", from_encoding="gbk")
            
            all_communitites = soup.find('div', attrs={'class':'key-list imglazyload'}).find_all("div", attrs={'class':'item-mod'})
            for xqItem in all_communitites:
                info_part = xqItem.find('div', attrs={"class":"infos"})

                # Skip non-sale communities
                try:
                    raw = info_part.find('div', attrs={"class":"tag-panel"}).get_text("", strip=True)
                    isOnsale = raw[0:2]
                except:
                    isOnsale = ''
                if isOnsale != '在售' or isOnsale == '':
                    continue

                # Source
                try:
                    source = '安居客'
                except:
                    source = ''

                # Current date
                try:
                    transDate = str(datetime.datetime.now().strftime('%Y-%m-%d'))
                except:
                    transDate = ''
                
                # URL, detail's URL, name 
                try:
                    url = xqItem['data-link']
                    detailed_url = url[0:-11] + 'canshu-' + url[-11:] + '?from=loupan_tab'
                    communityName = info_part.find('span', attrs={"class":"items-name"}).get_text("", strip=True)
                except:
                    detailed_url = ''
                    url = ''
                    communityName = ''

                # city, div, street
                try:
                    raw_address = info_part.find('span', attrs={"class":"list-map"}).get_text("", strip=True)
                    blank_counter = []
                    for index in range(0, len(raw_address)):
                        if raw_address[index] == raw_address[1]:
                            blank_counter.append(index)
                    city = city_name
                    div = raw_address[2:blank_counter[1]]
                    street = raw_address[(blank_counter[3]+1):]
                except:
                    city = ''
                    div = ''
                    street = ''

                # Price for reference
                try:
                    digit_part = xqItem.find('a', attrs={"class":"favor-pos"})
                    raw = digit_part.find('p', attrs={"class":"price"}).get_text("", strip = True)
                    unit1 = '元/㎡'
                    unit2 = '万元/套'
                    if unit1 in raw:
                        ref_unit = '元每平方米'
                    elif unit2 in raw:
                        ref_unit = unit2

                    ref_price = ''
                    for each in list(filter(str.isdigit, str(raw))):
                        ref_price += each
                except:
                    ref_unit = ''
                    ref_price = ''

                # type, floor
                try:
                    r = requests.get(detailed_url, headers = headers)    
                    pageStr = r.content
                    soup = BeautifulSoup(pageStr, "html.parser", from_encoding="gbk")

                    detail_info = soup.find_all('div', attrs={"class":"can-item"})[2].find('ul', attrs={"class":"list"}).find_all('li')

                    for each in detail_info:
                        if (each.find('div', attrs={"class":"name"}).get_text("", strip = True) == '建筑类型'):
                            levelType = each.find('div', attrs={"class":"des"}).get_text("", strip = True).strip("[查看详情]")

                        if (each.find('div', attrs={"class":"name"}).get_text("", strip = True) == '楼层状况'):
                            floors = each.find('div', attrs={"class":"des"}).get_text("", strip = True)
                        
                except:
                    levelType = ''
                    floors = ''

                # Extract all houses' type
                type_url = url[0:-11] + 'huxing-' + url[-11:] + '?from=loupan_tab'
                r = requests.get(type_url, headers = headers)    
                pageStr = r.content
                soup = BeautifulSoup(pageStr, "html.parser", from_encoding="gbk")
                try:
                    all_type = soup.find('ul', attrs={"class":"hx-list g-clear"}).find_all("li")
                    for each in all_type:
                        # Only on-sale house
                        if each.find('i', attrs={"class":"comm-stat zsale"}):
                            r = requests.get(each.find('a')['href'], headers = headers)    
                            pageStr = r.content
                            soup = BeautifulSoup(pageStr, "html.parser", from_encoding="gbk")
                            try:
                                type_detail = soup.find('div', attrs={"class":"hx-detail-wrap"}).get_text("", strip = True)
                            except:
                                type_detail = ''
                                
                            try:
                                price_detail = soup.find('span', attrs={"class":"total-price t-price-wrap"}).get_text("", strip = True)
                            except:
                                price_detail = ''
                            
                            try:
                                rooms_livings = getRoomsLivings(type_detail)
                                rooms = rooms_livings[0]
                                livings = rooms_livings[1]
                            except:
                                rooms = ''
                                livings = ''

                            try:
                                area = getArea(type_detail)
                            except:
                                area = ''

                            try:
                                orientation = getOrientation(type_detail)
                            except:
                                orientation = ''

                            try:
                                price_ = getPrice(price_detail, area)
                                totalPrice = price_[0]
                                unitPrice = price_[1]    
                            except:                      
                                unitPrice = ''
                                totalPrice = ''
                    
                            result.loc[len(result)] = [communityName, rooms, livings, area, orientation, levelType, floors, source, unitPrice, totalPrice, transDate, city, div, street, url, detailed_url, ref_price, ref_unit]
                except:
                    pass
            print('Page ' + str(i) + '/' + str(numPages) + ' parsing done')
        
        result.to_csv('Data/normalized/' + city_province + '/' + city_name + '.csv', index=False)
