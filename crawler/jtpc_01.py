
#========================================================================================
#=================这是这个静态爬虫小项目，爬取豆瓣top250电影，将其存在csv文件中=====================
#========================================================================================

import requests
import csv
import time
import random
from bs4 import BeautifulSoup

filename="豆瓣top250.csv"
url="https://movie.douban.com/top250"
headers = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"}

def clean_text(raw_text):#文本清洗，去掉多余空格、回车、制表符等
    if raw_text=="":
        return ""
    text=str(raw_text)
    text = text.replace("\xa0", "")
    text = text.replace("\n","")
    text = text.replace("\r","")
    text = text.replace("\t", "")
    text = " ".join(text.split())
    text = text.strip()
    return text

def csv_writer_w():#初始化csv表头
    with open(filename,"w",encoding="utf-8-sig",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["TOP排名","电影名称","电影地址"])
def csv_writer_a(data_list):#向csv写入数据
    with open(filename,"a",encoding="utf-8-sig",newline="") as f:
        writer=csv.writer(f)
        writer.writerows(data_list)

def get_page(url,headers,num):#爬虫主题代码
        try:
            db_movie=[]
            #time.sleep(random.uniform(1,2.5))
            response=requests.get(url,headers=headers,params={"start":num,"filter":""})#reponse是返回来的信息，用params去更改地址
            soup = BeautifulSoup(response.text,"html.parser")#将返回的信息解析以便后面跟好的寻找内容
            item_hd=soup.find_all("div",{"class":["hd"]})#soup.select("div.hd")  寻找div且class=hd（该代码包含电影名称与地址）的代码并保存
            I=1
            for i in item_hd:
                a_tag=i.find_all("a")#i.select("a")   在item中寻找<a>代码（就是电影的地址）
                s_tag=i.select("span.title")       #在item中寻找<span class==title>的代码（就是电影名称）
                title=clean_text(s_tag[0].text) #因为电影有很多名称，只取第一个（中文名称）
                link=clean_text(a_tag[0]["href"])#把地址取出来
                top=clean_text(num+I)#计算第几个电影
                db_movie.append([top,title,link])
                I=I+1
            return db_movie
        except requests.exceptions.RequestException as e:
            print(f"【网络异常】请求第{num+1}页失败：{e}")
            return []
        except Exception as e:
            print(f"【解析异常】请求第{num+1}页失败：{e}")
            return []
if __name__=="__main__":#防止调用时运行
    csv_writer_w()
    for num in range(0,250,25):#循环从1--250（因为发现每25个电影为一页，所以跨度为25）
        page_data=get_page(url,headers,num)
        if page_data!=[]:
            csv_writer_a(page_data)
            print(f"第{num/25+1}页，保存成功")
        else:
            print(f"第{num / 25 + 1}页，保失败")
            continue
    print("=========程序运行完成=========")