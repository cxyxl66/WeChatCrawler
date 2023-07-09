# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import json
import re
import pandas as pd
import pymysql


class WeixinSpider:
    def __init__(self):
        self.url_temp = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}


    def parse_url(self, url):  # 发送请求，获取响应
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()
    
    def get_content_list(self,html_str):#提取数据
        html = etree.HTML(html_str)
        content_list = []
        item = {}
        item["title"] = html.xpath("//*[@id=\"activity-name\"]/text()")
#         item["title"] = [i.replace("\n","").replace(" ","") for i in item["title"]]
        item["laiyuan"] = html.xpath("//*[@id=\"js_name\"]/text()")
#         item["laiyuan"] = [i.replace("\n","").replace(" ","") for i in item["laiyuan"]]
        item["other"] = html.xpath("//*[@id=\"js_content\"]//text()")
        print(item)
        content_list.append(item)

        return content_list

    def save_html(self, html_str, page_name):  # 保存html字符串
        file_path = "it/{}.html".format(page_name)
        with open(file_path, "w", encoding="utf-8") as f: 
            f.write(html_str)

    def get_url_list(self):
        file_path = "it.csv"
        df = pd.read_csv(file_path)
        temp_list = df["link"].str.split("!").tolist() #[[],[],[]]
        num_list = list(set([i for j in temp_list for i in j]))
        num_list_new = [i for i in num_list]
        
        time_list = df["create_time"].tolist() #[[],[],[]]
        return num_list_new,time_list

    def run(self):  # 实现主要逻辑
        # 1.构造url列表
        # 2.遍历，发送请求，获取响应
        url_list,time_list = self.get_url_list()
    
        # 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
        db = pymysql.connect("localhost", "root", "root", "weixin_database")
    
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
   
        for url in url_list:
            num = url_list.index(url)
            print(num)
            html_str = self.parse_url(url)
            content_list = self.get_content_list(html_str)
            title = ''.join(content_list[0]["title"])
            laiyuan = ''.join(content_list[0]["laiyuan"])
            other = '\n'.join(content_list[0]["other"])
            create_time = time_list[num]
            p = re.compile('<div class="rich_media_content " id="js_content">.*?</div>',re.S)
            html = re.search(p,html_str)
            if(html):
                html = re.search(p3,html_str).group().replace("\n","")
                
            else:
                html = html_str.replace("\n","")
            sql = """INSERT INTO weixin_table(title,url,other,html,create_time,type_id)
                VALUES ({},{},{},{},{},{},{},{})""".format('"'+title+'"','"'+url+'"','"'+other+'"',"'"+html+"'",create_time,1)
            try:
               # 执行sql语句
                cursor.execute(sql)
               # 提交到数据库执行
                db.commit()
            except:
                print("第"+num+"条数据插入失败")
               # 如果发生错误则回滚
                db.rollback()
               

            
            # 3.保存html
            page_name = title
            self.save_html(html_str, page_name)      
        # 关闭数据库连接
        db.close()


if __name__ == '__main__':
    weixin_spider = WeixinSpider()
    weixin_spider.run()
