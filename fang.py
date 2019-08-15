# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 21:32:27 2017

@author: Wensong Chu
"""
import sys, pickle

import DateRelatedUtils as dateTool
import parserTools as pTool

def parseStructure(theStr):

    theStr=theStr.strip()
    if theStr == u'平层':
        return 0
    elif theStr == u'开间':
        return 1
    elif theStr == u'跃层':
        return 2
    else:
        return -999

def parseDecoration(theStr):

    theStr=theStr.strip()
    if theStr==u'毛坯':
        return 0
    elif theStr==u'精装修':
        return 1
    elif theStr == u'中装修':
        return 2
    elif theStr == u'简装修':
        return 3
    elif theStr == u'豪华装修':
        return 4
    else:
        return -999

def parseOwnership(theStr):

    theStr=theStr.strip()
    if theStr==u'商品房':
        return 0
    elif theStr==u'使用权':
        return 1
    elif theStr == u'个人产权':
        return 2
    elif theStr == u'普通商品房':
        return 3
    else:
        return -999


def parsePropType(theStr):

    theStr=theStr.strip()
    if theStr==u'普通住宅':
        return 0
    elif theStr==u'豪华住宅':
        return 1
    else:
        return -999

def parseArchitect(theStr):

    theStr=theStr.strip()
    if theStr==u'板楼':
        return 0
    elif theStr==u'钢混':
        return 1
    elif theStr == u'塔楼':
        return 2
    elif theStr == u'平房':
        return 3
    elif theStr == u'砖混':
        return 4
    elif theStr == u'塔板结合':
        return 5
    else:
        return -999

def extratTitleInfo(oneString):

    threePieces = oneString.strip().split()
    name = threePieces[0]
    roomStr = threePieces[1]
    areaStr = threePieces[2]

    roomStr=roomStr.replace(u'室', '|')
    roomStr=roomStr.replace(u'厅','|')

    roomLiving = roomStr.split('|')

    if len(roomLiving)<2:
        print(oneString)
        room = -999
        living = -999
    else:
        room = pTool.getAFlaot(roomLiving[0])
        living = pTool.getAFlaot(roomLiving[1])

    areaStr = areaStr.replace(u'平米','')
    area = pTool.getAFlaot(areaStr)

    return name, room, living, area

def parseTitle(oneCol):

        communityName = []
        rooms = []
        livings = []
        area = []

        for oneString in oneCol:
            c, r, l, a = extratTitleInfo(oneString)
            communityName.append(c)
            rooms.append(r)
            livings.append(l)
            area.append(a)

        return communityName, rooms, livings, area

def parseLevelType(theStr):
    theStr = str(theStr)

    theStr = theStr.strip()
    if theStr.find('顶') >=0:
        return 3
    elif theStr.find('高') >= 0:
        return 2
    elif theStr.find('中') >= 0:
        return 1
    elif theStr.find('低') >= 0 or theStr.find('底')>=0:
        return 0
    elif theStr.find('地下')>=0:
        return -1
    else:
        return -999


def parseOritenation(theStr):

    try:
        theStr = theStr.strip()
        theStr = theStr.replace('向','|')
        theStr = theStr.replace(' ','|')
        theStr = theStr.replace('南','S')
        theStr = theStr.replace('北','N')
        theStr = theStr.replace('东','E')
        theStr = theStr.replace('西','W')
    except:
        theStr = ''

    return theStr.strip()

def parseLevels(theStr):
    theStr = str(theStr)

    theStr = theStr.strip()
    theStr = theStr.replace('共', '')
    theStr = theStr.replace('层', '')
    return pTool.getAFlaot(theStr)

def parseHouseFloor(oneCol):

    orientation = []
    levelTypes = []
    levels = []

    for oneString in oneCol:
        items = oneString.split('|')

        theOrientation = parseOritenation(items[0])
        theLevelType = parseLevelType(items[1])
        theLevelsPart = items[1].split('(')[1].strip(')')
        theLevels = parseLevels(theLevelsPart)

        orientation.append(theOrientation)
        levelTypes.append(theLevelType)
        levels.append(theLevels)

    return orientation, levelTypes, levels

def parseSource(theStr):
    theStr = str(theStr)

    theStr = theStr.strip()
    if theStr == '市场信息' or theStr=='其他公司成交':
        return 0
    elif theStr == '自行成交':
        return 1
    elif theStr == '房天下成交':
        return 2
    elif theStr == '链家成交':
        return 3
    elif theStr == '德佑成交':
        return 4
    else:
        return -999

def parseUnitPrice(theStr):
    theStr = str(theStr)

    theStr = theStr.strip()
    theStr = theStr.replace('元', '')
    return pTool.getAFlaot(theStr)

def parseTotalPrice(theStr):
    theStr = str(theStr)

    theStr = theStr.strip()
    theStr = theStr.replace('万', '')
    return pTool.getAFlaot(theStr)

def parseFangDotComColumns(inputFilename):

    theFile = open(inputFilename, 'rb')#pickle file
    theTape = pickle.load(theFile)

    #potential target columns
    targetColNames = ['communityName', 'rooms', 'livings', 'area', 'orientation', 'levelType', 'floors', 'source', 'unitPrice','totalPrice', 'transDate', 'city', 'div', 'street', 'url', 'detailedUrl']
    #targetColNames = ['rooms', 'livings', 'kitchens', 'baths', 'area', 'orientation', 'levelType', 'floors',
    #                  'source', 'buildingType', 'propType', 'houseRight', 'ownershipType', 'ownedByGroup',
    #                  'relatedSubway', 'houseHeatingType', 'buildingYear', 'decoType', 'withElevator', 'structure',
    #                  'floorType', 'transDate', 'latitude', 'longitude', 'city', 'div', 'numViewing', 'numFollowers', 'totalPrice',
    #                  'estPrice', 'numVisiting', 'numDaysToClose', 'numPriceAdj', 'unitPrice']

    #theTape = theTape.head(100)#sample
    communityName, rooms, livings, area = parseTitle(theTape['title'])
    theTape['communityName']=communityName
    theTape['rooms']=rooms
    theTape['livings']=livings
    theTape['area']=area

    orientation, levelTypes, levels = parseHouseFloor(theTape['house_floor'])

    theTape['orientation'] = orientation
    theTape['levelType'] = levelTypes
    theTape['floors'] = levels

    theTape = pTool.handleOneColumn(theTape, 'sale_source', 'source', parseSource)
    theTape = pTool.handleOneColumn(theTape, 'unit_price', 'unitPrice', parseUnitPrice)
    theTape = pTool.handleOneColumn(theTape, 'sale_price', 'totalPrice', parseTotalPrice)

    colDict = {'quyu_name':'div', 'city_name':'city',	'sale_time':'transDate', 'single_url':'url', 'detail_url':'detailedUrl', 'jiedao_name':'street'}
    theTape = theTape.rename(index=str, columns=colDict)



    return theTape, targetColNames


if __name__=='__main__':

    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]

    theTape, targetColName = parseFangDotComColumns(inputFilename)

    #print(targetColName)
    #print(theTape.columns)
    theTape[targetColName].to_csv(outputFilename, index=False, encoding='gb18030')

