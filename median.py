# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import math

if __name__ == '__main__':
    all_city = pd.read_csv('Data/city.csv', encoding = 'utf-8')
    prev_month = '2019-02'
    cur_month = '2019-07'
    median = []
    
    for all_index, all_row in all_city.iterrows():
        # current city
        city_name = all_row['city_name']
        city_province = all_row['city_province']
        print(city_name)

        path = 'Data/normalized/' + city_province + '/' + city_name + '.csv'
        current_city = pd.read_csv(path, encoding = 'utf-8')
        current_price = []

        # empty dataset
        if len(current_city) == 0:
            median.append(0.0)
            continue

        # record all prices and calculate median
        for index, row in current_city.iterrows():
            if row['ref_unit'] == '元每平方米':
                if math.isnan(row['unitPrice']) == False:
                    current_price.append(row['unitPrice'])
                elif math.isnan(row['ref_price']) == False:
                    current_price.append(row['ref_price'])
                else:
                    continue
            
            elif row['ref_unit'] == '万元/套':
                if math.isnan(row['unitPrice']) == False and math.isnan(row['area']) == False:
                    current_price.append(row['unitPrice']*10000 / row['area'])
                elif math.isnan(row['ref_price']) == False and math.isnan(row['area']) == False:
                    current_price.append(row['ref_price']*10000 / row['area'])
                else:
                    continue
            
            
        quantile_50 = np.percentile(current_price, 50)
        median.append(int(quantile_50) * 1.0)
        
    # add median to file
    p50 = pd.read_csv('Data/p50_padding.csv', encoding = 'utf-8')
    p50[cur_month] = median
    p50.to_csv('Data/p50_padding.csv', index=False)

    # modify nan data
    p50 = pd.read_csv('Data/p50_padding.csv', encoding = 'utf-8')
    for index, row in p50.iterrows():
        if row[cur_month] == 0.0:
            if math.isnan(row[prev_month]) == False:
                p50.loc[index, cur_month] = row[prev_month]
            else:
                continue
            
    p50.to_csv('Data/p50_padding.csv', index=False)