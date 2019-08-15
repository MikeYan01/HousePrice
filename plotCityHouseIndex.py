# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pandas as pd
import numpy, sys, matplotlib
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
import datetime, os

def oneBarOneChart(barDf, locationStr, barLocationStr):
    
    theDate=numpy.array(barDf['transDateYM'].tolist())
    # numPoints = len(barDf['transDateYM'])
    #theDate=numpy.array(range(numPoints))
    index = numpy.arange(len(theDate))

    theDateString =[]
    tempString = theDate.astype(str).tolist()
    for i in range(len(theDate)):
        theDateString.append(pd.to_datetime(tempString[i]).strftime('%b %Y'))
    theDateString=numpy.array(theDateString)

    theBarPrice_L=numpy.exp(barDf['p25'])
    theBarPrice_M=numpy.exp(barDf['p50'])
    theBarPrice_H=numpy.exp(barDf['p75'])
    #theChartPrice=numpy.exp(chartDf['M_5'])

    theTransactions = barDf['numTrans']
    
    FoneType=FontProperties("SimHei")
    matplotlib.rc('font', family='SimHei')
    
    barWidth = 0.15
    
    fig, ax2 = plt.subplots()

    #ax2.set_xticks(theDate)
    line1=ax2.bar(index-3*barWidth, theBarPrice_L, 2*barWidth, color='y')
    line2=ax2.bar(index-1*barWidth, theBarPrice_M, 2*barWidth, color='g')
    line3=ax2.bar(index+1*barWidth, theBarPrice_H, 2*barWidth, color='b')

    ax2.set_xlabel(u'年份', fontproperties=FoneType, fontsize=6)
    ax2.set_ylabel(u'元/平方米', fontproperties=FoneType, fontsize=6)
    ax2.set_xticks(index-0*barWidth)
    ax2.set_xticklabels(theDateString, rotation=70)
    ax2.set_xlim(min(index)-5*barWidth, max(index)+5*barWidth)

    ax1 = ax2.twinx()
    #line5=ax1.bar(theDate+2.5*barWidth, theTransactions, barWidth, color='c', alpha = 0.5)
    line5 = ax1.plot(index + 1.0 * barWidth, theTransactions, color='r')
    ax1.set_ylabel(u'交易量', fontproperties=FoneType, fontsize=6)

    ax2.legend((line1[0],line2[0],line3[0],line5[0]), (barLocationStr+' 25%中位',barLocationStr+' 50%中位',barLocationStr+' 75%中位', barLocationStr+' 交易量(右坐标）'), \
    loc='best',fontsize='x-small')

    for item in (ax1.get_xticklabels()):
        item.set_fontsize(6)

    ax1.tick_params(axis='y', labelsize=6)

    for item in (ax2.get_xticklabels()):
        item.set_fontsize(6)

    ax2.tick_params(axis='y', labelsize=6)

    plt.title(locationStr, fontproperties=FoneType,fontsize='large')
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.tight_layout()

    return fig

# def createProvinceBook(provinceIndex, outputFilename, levelString, onePage=None):
    
#     #nationalIndex=nationalIndex.sort_values('transDateYM')
#     #nationSummary = geoSummary[geoSummary.GeoCode==0]

#     allCityPages={}

#     with PdfPages(outputFilename) as pdf:

#         allProvinces = provinceIndex[levelString].unique()

#         if levelString == 'div':
#             pdf.savefig(onePage)

#         for p in allProvinces:

#             pIndex = provinceIndex[provinceIndex[levelString] == p]
#             if levelString=='city':
#                 locationStr = p
#             else:
#                 locationStr = provinceIndex.city.unique()[0] + "|" + p

#             theTitleStr=locationStr+u' 房产价格'
                
#             pIndex=pIndex.sort_values('transDateYM')
#             fig=oneBarOneChart(pIndex, theTitleStr, p)
#             pdf.savefig(fig)

#             if levelString=='city':
#                 allCityPages[p]=fig

#     return allCityPages

def createCityBook(cityIndex, outputFilename, city_name, onePage=None):
    cityPage={}

    with PdfPages(outputFilename) as pdf:
        theTitleStr = city_name + u' 房产价格指数'
            
        pIndex =cityIndex.sort_values('transDateYM')
        fig = oneBarOneChart(pIndex, theTitleStr, city_name)
        pdf.savefig(fig)

    return cityPage
            
def readNormalizedData(houseDataFile):

    theTape = pd.read_csv(houseDataFile, parse_dates=['date'], encoding = 'utf-8')
    theTape['transDateYM'] = theTape['date'].map(lambda theTape: theTape.replace(day=1))#normalize the date
    # theTape['logUnitPrice'] = numpy.log(theTape.price)
    theTape['logUnitPrice'] = theTape.price

    return theTape

def plotMajorCityIndex(theTape, outputFoldname, city_province, city_name, df1, df2):
    begDate = datetime.datetime(2016,3,1)
    endDate = datetime.datetime(2019,3,1)
    
    date_list = ['2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10',
    '2016-11', '2016-12', '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', 
    '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04',
    '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01',
    '2019-02']
    # outputPdfFilename = os.path.join(outputFoldname, (city_name + 'majorCityIndex_%s.pdf' % str(endDate)[:7]).replace('-', ''))

    theSummary = theTape.groupby(['transDateYM']).apply(lambda x: pd.Series(
        {'p25': x['logUnitPrice'].quantile(0.25), 'p50': x['logUnitPrice'].quantile(0.50), 'p75': x['logUnitPrice'].quantile(0.75), 'numTrans': x['logUnitPrice'].count() })).reset_index()

    line1 = []
    line1.append(city_province)
    line1.append(city_name)
    for i in range(0, len(date_list)):
        line1.append('')

    for i in range(0, len(date_list)):
        for index, row in theSummary.iterrows():
            if str(row['transDateYM'])[0:7] == date_list[i]:
                line1[i+2] = str( int(row['p50']) )

    df1.loc[ len(df1) ] = line1

    line2 = []
    line2.append(city_province)
    line2.append(city_name)
    for i in range(0, len(date_list)):
        line2.append('')

    for i in range(0, len(date_list)):
        for index, row in theSummary.iterrows():
            if str(row['transDateYM'])[0:7] == date_list[i]:
                line2[i+2] = str( int(row['numTrans']) )

    df2.loc[ len(df2) ] = line2

    # allCityPages = createCityBook(theSummary[(theSummary['transDateYM']>=begDate) & (theSummary['transDateYM']<endDate)], outputPdfFilename, city_name)
    # return allCityPages

# def plotEachCityIndex(theTape, outputFoldname, allCityPages):

#     begDate = datetime.datetime(2015,1,1)
#     endDate = theTape['transDateYM'].max()

#     theSummary = theTape.groupby(['transDateYM']).apply(lambda x: pd.Series(
#         {'p25': x['logUnitPrice'].quantile(0.25), 'p50': x['logUnitPrice'].quantile(0.50), 'p75': x['logUnitPrice'].quantile(0.75), 'numTrans': x['logUnitPrice'].count() })).reset_index()

#     theSummary = theSummary[(theSummary['transDateYM']>=begDate) & (theSummary['transDateYM']<endDate)]

#     allCities = theTape['city'].unique()
#     for p in allCities:
#         theFilename = os.path.join(outputFoldname, 'city_%s.pdf' % p)
#         createCityBook(theSummary[theSummary.city==p], theFilename, 'div', allCityPages[p])


if __name__=='__main__':
    all_city = pd.read_csv('city.csv', encoding = 'utf-8', error_bad_lines=False)
    
    df1 = pd.DataFrame(columns = ['province', 'city', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12', '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', 
    '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04',
    '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01',
    '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07'])

    df2 = pd.DataFrame(columns = ['province', 'city', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12', '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', 
    '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04',
    '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01',
    '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07'])

    for index, row in all_city.iterrows():
        city_name = row['city_name']
        city_province = row['city_province']
        print(city_name)

        path = 'Data/final_price_padding/' + city_province + '/' + city_name + '价格/'
        houseDataFile = path + city_name + '.csv'
        outputFoldname = 'Data/price_index/' + city_province + '/' + city_name
        if os.path.exists(outputFoldname):
            pass
        else:
            os.makedirs(outputFoldname)


        theTape = readNormalizedData(houseDataFile)
        plotMajorCityIndex(theTape, outputFoldname, city_province, city_name, df1, df2)
        # plotEachCityIndex(theTape, outputFoldname, allCityPages)


    df1.to_csv('Data/p50_padding.csv', index = False)
    df2.to_csv('Data/transaction_padding.csv', index = False)