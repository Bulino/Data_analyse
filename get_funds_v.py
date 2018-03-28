# !/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

import tushare as ts
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
# from pylab import mpl
# from matplotlib import font_manager

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.family'] = 'DejaVu Sans'

# plt.rcParams['font.sans-serif'] = ['SimHei']
#
#
# def getChineseFont():
#      matplotlib库根本不支持下面字体
#     return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
#
#
# fontP = font_manager.FontProperties()
# fontP.set_family('SimHei')
# fontP.set_size(14)


if os.path.exists('./t1.csv') and os.path.exists('./t2.csv') and \
        os.path.exists('./t3.csv'):

    t1 = pd.read_json('t1.csv')
    t2 = pd.read_json('t2.csv')
    t3 = pd.read_json('t3.csv')
else:

    t1 = ts.fund_holdings(2017, 1)
    t2 = ts.fund_holdings(2017, 2)
    t3 = ts.fund_holdings(2017, 3)
    with open('t1.csv', 'w') as f:
        f.write(t1.to_json())
    with open('t2.csv', 'w') as f:
        f.write(t2.to_json())
    with open('t3.csv', 'w') as f:
        f.write(t3.to_json())


t1.columns = t1.columns.str.replace('nums', 'nums1')
t2.columns = t2.columns.str.replace('nums', 'nums2')
t3.columns = t3.columns.str.replace('nums', 'nums3')

r1 = pd.merge(t1, t2 ,on='code', how='left')
r2 = pd.merge(r1, t3, on='code', how='left')

g_data = (r2[(r2['nums3'] > r2['nums2'])&(r2['nums2'] > r2['nums1'])]
          [['code', 'name', 'nums3', 'nums2', 'nums1']].sort_values(
    by=['nums3']).drop_duplicates(['code']))

means_first = g_data['nums1'].values.tolist()
means_frank = g_data['nums2'].values.tolist()
means_guido = g_data['nums3'].values.tolist()

n_groups = len(g_data)


fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rect1 = plt.bar(index, means_frank, bar_width,
                color='b',label='2季度基金持股',
                alpha=opacity)
rect2 = plt.bar(index + bar_width, means_guido, bar_width,
                color='g', label='3季度基金持股',
                alpha=opacity)
rect3 = plt.bar(index - bar_width, means_first, bar_width,
                color='y', label='3季度基金持股',
                alpha=opacity)

plt.xlabel('股票名称',)
plt.ylabel('持股基金')
plt.title('2017年1，2，3季度基金持股加强情况')
plt.setp(ax.get_xticklabels(), color='r')

title_col = g_data['name'].values.tolist()

plt.xticks(index + bar_width, title_col, rotation='vertical',
           verticalalignment='bottom')
plt.legend(loc=2)

plt.tight_layout()
plt.show()
# plt.savefig('Funds_V.png', bboxsize='tight')