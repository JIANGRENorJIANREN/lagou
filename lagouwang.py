#-*- coding:utf-8 -*-

import requests
import json
import pandas as pd
import re

header = {
    'Host': 'www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.lagou.com/jobs/list_python?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'X-Anit-Forge-Code': '0',
    'Content-Length': '26',
    'Cookie':'_ga=GA1.2.1529817955.1515920383; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520133971,1520138032,1520604328,1520686278; user_trace_token=20180114165942-4292a8f7-f909-11e7-a2f4-5254005c3644; LGUID=20180114165942-4292aebc-f909-11e7-a2f4-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=13; gate_login_token=a60ccd2b9f8ed1547d8faa9620ea8b980cfbadcd179eab59; index_location_city=%E6%88%90%E9%83%BD; _gid=GA1.2.1666659613.1520604328; SEARCH_ID=01c2db1a84cc4d42baf18fa92618de4f; _gat=1; LGSID=20180310205118-b9f1a15e-2461-11e8-a8b2-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fword%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26tn%3D50000022_hao_pg%26ie%3Dutf-8%26sc%3DUWd1pgw-pA7EnHc1FMfqnHRznjm3PHbsnHTdPauW5y99U1Dznzu9m1Yvn1DvPW0zPHn%26ssl_sample%3Ds_4%26srcqid%3D1834243118515327763%26f%3D3%26rsp%3D0; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; LGRID=20180310205154-cf6e84ba-2461-11e8-a8b4-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520686314; _putrc=D118D830675919EE; JSESSIONID=ABAAABAAAGGABCB875851FA0522DA5442B3A4478B1CC358; login=true; unick=%E7%8E%8B%E9%A3%9E; hideSliderBanner20180305WithTopBannerC=1; TG-TRACK-CODE=index_search',
    'Connection': 'keep-alive'
}


def download(url):
    for i in range(1, 31):
        form_data = {'first': 'false', 'kd': 'python', 'pn': str(i)}
        html = requests.post(url, data=form_data, headers=header).text
        try:
            ajax = json.loads(html)
        except ValueError as e:
            print(e)
            ajax = None
        else:
            result = ajax['content']['positionResult']['result']
            df = pd.DataFrame(result)   #DataFrame可直接将dict转换为df格式
            #保存到本地
            df_selected = df.ix[:, ['companyFullName', 'city', 'companyLabelList', 'companySize', 'createTime', 'district',
                                    'education', 'financeStage', 'firstType', 'industryField', 'positionAdvantage',
                                    'positionLables', 'positionName', 'salary', 'workYear']]
            df_selected.to_csv('/home/wangf/PycharmProjects/tianmaoScrape/lagouwang_datas.csv', index=True, mode='a+')


#可视化部分
import pandas as pd              #数据框操作
import numpy as np
import matplotlib as mpl         #配置字体
mpl.use('TkAgg')
import matplotlib.pyplot as plt  #绘图
import jieba                     #分词
from wordcloud import WordCloud  #词云可视化
from pyecharts import Geo        #地理图

def data_view(file_path):
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    #配置绘图风格
    plt.rcParams['axes.labelsize'] = 16.
    plt.rcParams['xtick.labelsize'] = 14.
    plt.rcParams['ytick.labelsize'] = 14.
    plt.rcParams['legend.fontsize'] = 12.
    plt.rcParams['figure.figsize'] = [15., 15.]

    #读取数据
    datas = pd.read_csv('/home/wangf/PycharmProjects/tianmaoScrape/lagouwang_datas.csv', encoding='utf-8')

    #学历要求
    datas['education'].value_counts().plot(kind='bar', rot=0)
    plt.show()

    #工作年限
    datas['workYear'].value_counts().plot(kind='barh', rot=0)
    plt.show()

    #工作地点
    datas['city'].value_counts().plot(kind='pie', autopct='%1.2f%%', explode=np.linspace(0.0, 0.6, 21))
    plt.show()

    #热门岗位
    final = ''
    stopwords = ['PYTHON', 'Python', 'python', '工程师', '(',')', '/']   #停止词
    for i in range(datas.shape[0]):
        seg_list = list(jieba.cut(datas['positionName'][i]))
        for seg in seg_list:
            if seg not in stopwords:
                final = final + seg + ' '

    #工作地理图
    #提取数据框
    #data2 = list(map(lambda x: (datas['city'][x], eval(re.split('k|K', datas['salary'][x])[0])*1000), range(len(datas))))
    #提取工资信息
    #data3 = pd.DataFrame(data2)
    #转化成Geo需要的格式
    #data4 = list(map(lambda x: (data3.groupby(0).mean()[1].index[x], data3.groupby(0).mean()[1].values[x]), range(len(data3.groupby(0)))))
    #地理位置展示
    #geo = Geo('xxxxx', 'yyyyy', title='#fff', title_pos='left', width=1200, height=600, background_color='#404a59')
    #attr, value = geo.cast(data4)
    #geo.add('', attr, value, type='heatmap', is_visualmap=True, visual_range=[0, 300], visual_text_color='#fff')
    #geo







if __name__ == '__main__':
    #下载数据
    #url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    #download(url)

    #数据可视化
    path = '/home/wangf/PycharmProjects/tianmaoScrape/lagouwang_datas.csv'
    data_view(path)
