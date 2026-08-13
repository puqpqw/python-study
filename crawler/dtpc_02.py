#本爬虫是以学习为目的，不存在恶意盗取信息
#代码来源：本人在看动画的时候感觉加载很慢，在想能不能设计一个爬虫把漫画都下载下来方便观看
#思考：在测试时发现有时网络问题使得后面的图片先加载出来导致捕捉顺序错乱，但该网站的图片地址用了blob加密，最后只能动态抓取，用image_num调整顺序
#不足：image_num不是一成不变的，后面的几章会改变，如果能弄一个自动捕捉编写image_num代码的函数就好了，但是能力有限暂时还无法写出来
import os
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

#先建立一个文件夹，如果没有就建立，有就跳过，用来存放章节文件夹
save_dir = "my_images"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

#我发现所爬取的url最后9位对应着它们各自图片位置，这个是帮助图片命名，在网络不好先接收后面图片时让顺序不乱（需要更改，不是一成不变的）
image_num={"xLndlYnA=":0,
           "yLndlYnA=":1,
           "zLndlYnA=": 2,
           "0LndlYnA=": 3,
           "1LndlYnA=": 4,
           "2LndlYnA=": 5,
           "3LndlYnA=": 6,
           "4LndlYnA=": 7,
           "5LndlYnA=": 8,
            "xMC53ZWJw":9,
           "xMS53ZWJw": 10,
           "xMi53ZWJw": 11,
           "xMy53ZWJw": 12,
            "xNC53ZWJw":13,
           "xNS53ZWJw": 14,
           "xNi53ZWJw": 15,
           "xNy53ZWJw": 16,
            "xOC53ZWJw":17,
           "xOS53ZWJw": 18,
           "yMC53ZWJw":19,
           "yMS53ZWJw": 20,
           "yMi53ZWJw": 21,
           "yMy53ZWJw": 22,
           "yNC53ZWJw":23
           }


dh_page_num=int(input("想要从哪章爬取"))
dh_page_nummax=int(input("想要爬到哪章"))
#这个是我在网上看动画的网站
Url=f"https://www.duokanmh.com/manhua/m9yj09O1M5/{dh_page_num}.html"
#头文件
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0",
}
#抓取的页数
page_image_num=[0]
#自动识别是否到底部
def is_scroll_bottom(page):
    res = page.evaluate("""
        ()=>{
            let scrollY = window.scrollY;
            let view_height = window.innerHeight;
            let total_height = document.documentElement.scrollHeight;
            return scrollY + view_height >= total_height - 10;
        }
    """)
    return res

#主函数
if __name__=="__main__":
    with sync_playwright() as a:
        browser = a.chromium.launch(headless=False)
        context_01=browser.new_context(extra_http_headers=headers)
        page = context_01.new_page()

        #监听函数
        def on_response(reponse):
            #nonlocal page_image_num
            #创建对应的章节，为子文件
            file_name=f"第{dh_page_num}章"
            sub_dir=os.path.join(save_dir,file_name)
            os.makedirs(sub_dir,exist_ok=True)
            #开始爬取图片
            url=reponse.url
            #"https://two.mhpic.net/"是我发现只要是动漫图片都含有这个地址
            if "https://two.mhpic.net/" in url:
                #获得对应的编号以便命名对应的顺序
                if url[-9] in image_num:
                    image = image_num[url[-9:]]
                    rep=reponse.body()
                    #将图片放入对应的子文件夹中
                    get_image=os.path.join(sub_dir, f"{image}.jpg")
                    with open(get_image, "wb") as f:
                        f.write(rep)
                    print(f"成功写入第{image}张")
            #抓取到的照片数加一，方便后面判断有没有抓取全面
            page_image_num[0]+=1
        #动态浏览界面函数
        page.on("response", on_response)
        while(dh_page_num <= dh_page_nummax):
            i=0
            #爬取的对应网页地址
            url = f"https://www.duokanmh.com/manhua/m9yj09O1M5/{dh_page_num}.html"
            page.goto(url)   #url
            page.wait_for_timeout(7000)
            #如果没有到底
            while not is_scroll_bottom(page):
                #i: 滚动到的照片层数
                i+=1
                page.wait_for_timeout(2000)
                    # 如果不相等，则意味翻到的页数跟抓取页数不一样，选择等待加载一下
                if page_image_num[0] <= i:
                    page.wait_for_timeout(2000)
                    if page_image_num[0] <= i:
                        page.wait_for_timeout(2000)
                # 持续滚动，直到页面底部

                # 向下滚动一屏，因为我学习的网站图片滚动两下到下一个图片，所以选择了滚动两下
                page.evaluate("window.scrollBy(0, window.innerHeight)")
                page.evaluate("window.scrollBy(0, window.innerHeight)")
            dh_page_num+=1
            #清零方便下一次记录
            page_image_num[0]=0

        browser.close()