import pandas as pd
import sys, os

def retrieve_locations(df):
    convert_date = []
    for index, row in df.iterrows():
        convert_date.append(row['date'])
    return convert_date

def search_padding_dates(convert_date, date_list):
    result_date_list = []

    # Only one record, and determine whether to pad date
    if len(convert_date) == 1:
        for each in date_list:
            if each > convert_date[0]:
                result_date_list.append(each)

    # Otherwise, check all records and determine where to pad date
    else:
        for i in range(0, len(convert_date)-1):
            for each in date_list:
                if each > convert_date[i] and each < convert_date[i+1]:
                    result_date_list.append(each)
        
        for each in date_list:
            if each > convert_date[len(convert_date)-1]:
                result_date_list.append(each)
    
    return result_date_list


if __name__=='__main__':
    date_list = ['2016-03-01', '2016-04-01', '2016-05-01', '2016-06-01', '2016-07-01', '2016-08-01', '2016-09-01', '2016-10-01', '2016-11-01', '2016-12-01', '2017-01-01', '2017-02-01', '2017-03-01', '2017-04-01', '2017-05-01', '2017-06-01', '2017-07-01', 
    '2017-08-01', '2017-09-01', '2017-10-01', '2017-11-01', '2017-12-01', '2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01',
    '2018-05-01', '2018-06-01', '2018-07-01', '2018-08-01', '2018-09-01', '2018-10-01', '2018-11-01', '2018-12-01', '2019-01-01',
    '2019-02-01']

    all_city = pd.read_csv('Data/city.csv', encoding = 'utf-8', error_bad_lines=False)
    for index, row in all_city.iterrows():
        city_name = row['city_name']
        city_province = row['city_province']
        print(city_name)

        path = 'Data/final_price_padding/' + city_province + '/' + city_name + '价格/'
        for theFile in os.listdir(path):
            # Skip unrelated files
            if theFile == '.DS_Store' or theFile == (city_name + '.csv'):
                continue
            theTape = pd.read_csv(path + theFile, encoding = 'utf-8', error_bad_lines=False)
            
            # Skip null records
            if len(theTape) == 0:
                continue

            # Pad dates
            convert_date = retrieve_locations(theTape)
            result_date_list = search_padding_dates(convert_date, date_list)

            for each in result_date_list: 
                theTape.loc[ len(theTape) ] = [each, '', '元每平方米']

            theTape = theTape.sort_values(by = ['date'])
            
            last_price = ''
            for index, row in theTape.iterrows():
                if row['price'] != '':
                    last_price = str(row['price'])
                else:
                    theTape.loc[index, 'price'] = str(last_price)

            theTape.to_csv(path + theFile, index=False)
            