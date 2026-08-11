from multiprocessing import context
from re import search

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"}

# sync_playwright() 启动 Playwright 底层服务；
# as a：把生成的管理器赋值给变量 a；
# 通过 a.chromium 调用 Chromium 浏览器引擎（还支持 a.firefox()、a.webkit()）；
with sync_playwright() as a:#a相当于一个管理器可以启动浏览器（可以启动多个）
    browser = a.chromium.launch(headless=False)#启动chromium浏览器，（launch==常用于“启动”屏幕）
    context_01=browser.new_context(extra_http_headers=headers)#创建上下文可以记住headers和cookie等信息（可以有多个不同的）：如下
    context_02=browser.new_context(extra_http_headers=headers)   #其中headers可为其他的
    page = context.new_page()#打开一个界面
    page.goto("https://movie.douban.com/top250?start=0")    #他们的User-Agent等信息都不一样
    page.goto("https://www.baidu.com")#跳转到百度搜索界面
    search_input=page.locator("#chat-textarea")##chat-textarea是百度搜索框的id，（locator==定位器）：定位到搜索框
    search_input.fill("bilibili")#填充“bilibili”这个搜索词
    page.locator("#chat-submit-button").click()#定位到搜索按钮的idchat-submit-button，（click==点击）：点击搜索按钮
    browser.close()#关闭chromium浏览器
