# Brief Introduction   

A Python project to collect Chinese real estate's information on the Internet and train a model to precict house price.    

# File Structure    
    .
    ├── anjuke.py    Collect and normalize data from Anjuke
    ├── fang.py    Collect and normalize data from Fang
    ├── lianjia.py    Normalize data from Lianjia
    ├── median.py    Calculate the median of a city's house prices   
    ├── padding.py    Pad price between records     
    ├── plotCityHouseIndex.py    Generate each city's HPI chart book, or general sheet     
    ├── train.ipynb    Train a model of house price and make predictions using scikit-learn & Tensorflow
    └── util.py    Some trivial functions used in data wrangling

# Source of Information   

[安居客](https://www.anjuke.com/)    
[房天下](https://www.fang.com/)     
[链家](https://www.lianjia.com)     