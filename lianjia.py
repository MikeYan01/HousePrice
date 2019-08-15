# -*- coding: utf-8 -*-
import os
import pandas as pd
import math
import re
import numpy as np
import json
import _geohash

# Filter raw data
def filter(data, input_hash):
    # find all near communities by hashcode
    try:
        data = data[data.geohash.str[:5] == input_hash[:5]]
    except:
        data = data

    return data

# In the same grid or in neighboring grids
def in_range(input_hash, input_hash_neighbors, ref_hash):
    if input_hash[:6] == ref_hash[:6]:
        return True
    if ref_hash in input_hash_neighbors:
        return True
    return False


# Normalize format according to HPI
def modify_price(HPI_reference, input_city, input_div, record_price, record_date):
    refer_data = HPI_reference[HPI_reference['city'] == input_city]
    refer_data = HPI_reference[HPI_reference['div'] == input_div]

    earliest_date = refer_data.iloc[0,0]
    latest_date = refer_data.iloc[-1,0]
    latest_price = refer_data.iloc[-1, 5]

    
    if record_date < earliest_date:
        record_date = earliest_date
    elif record_date > latest_date:
        record_date = latest_date
    else:
        record_date = record_date[0:-2] + '01'
    
    
    if record_date == latest_date:
        return record_price
    else:
        for index, row in refer_data.iterrows():
            if record_date == row['transDateYM']:
                prev_price = row['p50']
                if (math.isnan(record_price)):
                    record_price = latest_price
                if (math.isnan(prev_price)):
                    prev_price = latest_price
                
                modified_price = latest_price * 1.0 / prev_price * record_price
                return int(modified_price)


if __name__ == '__main__':
    
    # city = ['上海', '北京', '南京', '厦门', '合肥', '广州', '成都', '杭州', '武汉', '济南', '深圳', '烟台', '石家庄', '苏州', '西安', '重庆', '长沙', '青岛']

    city_name = '重庆'
    
    raw_data = pd.read_csv('Data/city_split/' + city_name + '.csv', encoding = 'utf-8')
    data = raw_data.sort_values(by = 'geohash')
    data.reset_index(drop=True, inplace=True)
    length = len(data)

    HPI_reference = pd.read_csv('Data/index.csv', encoding = 'utf-8')

    all_quantile_50 = []
    quantile_50_cache = 0.00

    last_row = ''

    for index, row in data.iterrows():
        input_name = row['geohash'][:5]

        if (index % 1000 == 0):
            print(str(index) + '/' + str(length))
        
        # In the same community as the last record
        if last_row == input_name:
            last_row = input_name
            all_quantile_50.append( quantile_50_cache )
            continue
        else:
            last_row = input_name
            
            input_hash = row['geohash']
            input_hash_neighbors = [each[:6] for each in _geohash.neighbors(input_hash)]
            input_city = row['city']
            input_div = row['div']
            
            price = []

            filtered_data = filter(data, input_hash)
            
            for filtered_index, filtered_row in filtered_data.iterrows():
                ref_hash = filtered_row['geohash']
                if (in_range(input_hash, input_hash_neighbors, ref_hash)):

                    record_price = filtered_row['unitPrice']
                    record_date = filtered_row['transDate']

                    # Modify price
                    modified_price = modify_price(HPI_reference, input_city, input_div, record_price, record_date)
                    price.append(modified_price)

            # Update cache              
            price = np.array(price)
            quantile_50_cache = '%.2f' % np.percentile(price, 50)
            all_quantile_50.append( quantile_50_cache )

        
    data['quantile_50'] = all_quantile_50
    data.to_csv('Data/city_result/' + city_name + '.csv', index=False)
