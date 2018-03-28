# !/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import importlib            #加强版import

# importlib.reload(sys)     #python文档不推荐加载sys等系统模块

import os
import pandas as pd
import quandl
import pickle
import matplotlib.pyplot as plt
import plotly.offline as py #IPython绘图库，离线绘图
import plotly.figure_factory as ff
import plotly.graph_objs as go


py.init_notebook_mode(connected=True)   #必须安装jupyter才能在pycharm中使用


def get_quandl_data(quandl_id):
    """Download and cache a Quandl datarises"""
    #存储获取的数据结构路径
    cache_path = '{}.pkl'.format(quandl_id).replace('/', '-')
    try:
        f = open(cache_path, 'rb')  #打开路径代表的文件,一字节流的形式读取
        df = pickle.load(f)         #加载文件对象到变量
        print('Loaded {} from cache'.format(quandl_id))     #打印提示
    except(OSError, IOError) as e:
        print('Downloading {} from Quandl'.format(quandl_id))
        df = quandl.get(quandl_id, returns='pandas')    #以pandas方式返回数据集
        df.to_pickle(cache_path)                        #转换为pickle 格式
        print('Cache {} at {}'.format(quandl_id, cache_path))
    return df       #记得返回值，否则下述代码会出现空类型

if __name__ == '__main__':
    #掉用函数并绘图
    btc_usd_price_kraken = get_quandl_data('BCHARTS/KRAKENUSD')#调用函数获取数据
    #通过rolling_mean函数进行指定窗口大小的列数据，计算简单算数平滑移动平均线，指数平滑移动平均线用ewma
        #五日均线就是前五日（五个窗口的收盘价）的平滑移动平均数
    btc_usd_price_kraken['ma5'] = pd.rolling_mean(btc_usd_price_kraken[
                                                     'Close'], 5)
    btc_usd_price_kraken['ma20'] = pd.rolling_mean(btc_usd_price_kraken[
                                                      'Close'], 20)
    list_f = ['ma5', 'ma20', 'Close','Volume (BTC)']    #关键字组成的列表
    print(btc_usd_price_kraken.head())

    btc_usd_price_kraken[list_f].plot()     #关键字组成的列表代表的数据绘图
    plt.legend(loc=2)
    plt.title("The Price of BTC Trend in Kraken", fontsize=16)
    plt.grid(b=True)

    plt.show()
    # plt.savefig('BTC.png', bbox_inchse='tight')