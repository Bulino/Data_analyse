# !/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Attempt to make a graph compare with some stocks
"""

import os
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt

# Align the stock and the name for reader of module 'data'
dic = {'谷歌': 'GOOG', '亚马逊': 'AMZN', '脸书': 'FB',
        '阿里巴巴': 'BABA', '腾讯': '0700.hk', '苹果': 'AAPL', }

# Set the date
start_date = '2017-1-1'
end_date = '2018-1-1'

# Attempt to check the files, if it does'n exit,try to get it.
if (os.path.exists('./google_to.csv') and os.path.exists('./Amazon_to.csv') and
    os.path.exists('./FB_to.csv') and os.path.exists('./ali_to.csv') and
    os.path.exists('./apple_to.csv') and os.path.exists('./tencent_to.csv')
    ):
    dateparse1 = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')

    d_g = pd.read_csv('./google_to.csv',skiprows=0, index_col='Date',
                      date_parser=dateparse1, parse_dates=True,
                      )
    d_am = pd.read_csv('./Amazon_to.csv', skiprows=0, index_col='Date',
                       date_parser=dateparse1, parse_dates=True,
                       )
    d_f = pd.read_csv('./FB_to.csv', skiprows=0, index_col='Date',
                      date_parser=dateparse1, parse_dates=True,
                      )
    d_a = pd.read_csv('./apple_to.csv', skiprows=0, index_col='Date',
                      date_parser=dateparse1, parse_dates=True,
                      )
    d_ten = pd.read_csv('./tencent_to.csv', skiprows=0, index_col='Date',
                        date_parser=dateparse1, parse_dates=True,
                        )
    d_baba = pd.read_csv('./ali_to.csv', skiprows=0, index_col='Date',
                         date_parser=dateparse1, parse_dates=True,
                        )
else:
    d_g = data.get_data_yahoo(dic['谷歌'], start_date, end_date)
    try:
        with open('./google_to.csv', 'w') as f:
            f.write(d_g.to_csv())
    except IOError:
        print ("Please check your code,dedicate space.")
    else:
        d_g.head()      #文件操作后会释放变量，这一行在执行时并不显示

    d_am = data.get_data_yahoo(dic['亚马逊'], start_date, end_date)
    try:
        with open('./Amazon_to.csv', 'w') as f:
            f.write(d_am.to_csv())
    except IOError:
        print ("Please check your code,dedicate space.")
    else:
        pass

    d_f = data.get_data_yahoo(dic['脸书'], start_date, end_date)
    try:
        with open('./FB_to.csv', 'w') as f:
            f.write(d_f.to_csv())
    except IOError:
        print ("Please check your code,dedicate space.")
    else:
        pass

    d_a = data.get_data_yahoo(dic['苹果'], start_date, end_date)
    try:
        with open('./apple_to.csv', 'w') as f:
            f.write(d_a.to_csv())
    except IOError:
        print ("Please check your code,dedicate space.")
    else:
        pass

    d_ten = data.get_data_yahoo(dic['腾讯'], start_date, end_date)
    try:
        with open('./tencent_to.csv', 'w') as f:
            f.write(d_ten.to_csv())
    except IOError:
        print ("Please check your code,dedicate space.")
    else:
        pass

    d_baba = data.get_data_yahoo(dic['阿里巴巴'], start_date, end_date)
    try:
        with open('./ali_to.csv', 'w') as f:
            f.write(d_baba.to_csv())
    except IOError:
        print ("Please check your code,dedicate space.")
    else:
        pass


def c_ratio(d_close):
    """
    analyse the increment ratio of a stock
    :param d_close:
    :return: a num
    """
    o_price = d_close.Close[0]
    c_price = d_close.Close[-1]

    # o_price = d_close['Close'][0]
    # c_price = d_close['Close'][-1]

    ratio = '%.2f%%' % (round(((c_price - o_price) / o_price), ndigits=4) * 100)

    return ratio

# print(c_ratio(d_g))

# Set the font to support Chinese
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Let's visual
fig = plt.figure(dpi=128, figsize=(10, 6))
# d_g['date'] = d_g.index
# plt.plot(d_g['date'], d_g['Close'], color='r',
#          label='Google'+ '^' + str(c_ratio(d_g)))
d_g['Close'].plot(label="Google" + '^' + str(c_ratio(d_g)))
d_am['Close'].plot(label='Amazon' + '^' + str(c_ratio(d_am)))
d_f['Close'].plot(label='Facebook' + '^' + str(c_ratio(d_f)))
d_a['Close'].plot(label='Apple' + '^' + str(c_ratio(d_a)))
d_ten['Close'].plot(label='Tencent' + '^' + str(c_ratio(d_ten)))
d_baba['Close'].plot(label='Alibaba' + '^' + str(c_ratio(d_baba)))

plt.title('2017GAFATA组合股价年增长趋势', fontsize=20)
plt.xlabel('日  期', fontsize=16)
plt.ylabel('收盘价格', fontsize=16)
plt.tick_params(axis='both', labelsize=12, which='major')
plt.grid(True)
plt.legend(loc='best')

plt.show()
# plt.savefig('GAFATA.png', bbox='tight')