import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
}


def getHTMLText(url):
    try:
        r=requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return 'error'

title_list=[]#标题列表
address_list=[]#地址列表
shape_list=[]#户型面积列表
money_list=[]#价格列表
href_list=[]#链接列表
feature_list=[]#特点列表

start_url="http://sh.ganji.com/fang1/b2000e5000m1"

print('ready to get')
for i in range(1,60):
    url=start_url+'o'+str(i)+'/_转租/'
    html=getHTMLText(url)
    print(url)


    soup=BeautifulSoup(html,'html.parser')

    title=soup.find_all('dd',attrs={"class":"dd-item title"})#标题
    for i in title:
        title_list.append(i.text.replace(' ','').replace('\n',''))
    address=soup.find_all("dd",attrs={"class":"dd-item address"})#地址
    for i in address:
        address_list.append(i.text.replace(' ','').replace('\n',''))
    shape=soup.find_all('dd',attrs={"class":"dd-item size"})#房型
    for i in shape:
        shape_list.append(i.text.replace(' ','').replace('\n',''))
    money=soup.find_all('div',attrs={"class":"price"})#价格
    for i in money:
        money_list.append(i.text.replace('\n',''))
    href=soup.select('a[class="js-title value title-font"]')
    feature=soup.find_all('dd',attrs={"class":"dd-item feature"})
    for i in feature:
        feature_list.append(i.text.replace('\n', ''))
    for i in href:#链接
        newhref=i.get('href')
        if 'zhiding.html' in newhref:
            continue
        href_list.append('http://sh.ganji.com/'+newhref)



#字典中的key值即为csv中列名
dataframe = pd.DataFrame({'标题':title_list,'地址':address_list,'房型':shape_list,'价格':money_list,'特点':feature_list,'链接':href_list})
# # #将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_csv("转租(赶集网).csv",index=False,sep=',')

# a=0
# for i in range(len(title_list)):
#
#     print(title_list[a])
#     print(address_list[a])
#     print(shape_list[a])
#     print(money_list[a])
#     print(feature_list[a])
#     print('链接地址：'+href_list[a]+'\n')
#     a=a+1
