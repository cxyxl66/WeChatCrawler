# -*- coding: UTF-8 -*-
import requests
import time
import pandas as pd
import math
import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",
]

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
cookie = "appmsglist_action_3211828736=card; ua_id=xf1IJPpCxrOkzx7HAAAAAEfpoLhrY0vf20LrgWcLYec=; wxuin=86999637334436; mm_lang=zh_CN; sig_login=h01d1e20db4fb703b033225cbbdba00bbe3cdc4ec6e572a379ee6538c8469a1e7fb7fa70fbab1502f6e; poc_sid=HKiMpWSj06-7f7D34kNWA1XMhli1chB19UDerP16; rewardsn=; wxtokenkey=777; _clck=3211828736|1|fd4|0; uuid=f96f4e9ebfb016ffe047415406c68016; rand_info=CAESIFj8UW/i916e5Wjx44FVtePMf/z26P4BzVg7WkY8+mZ3; slave_bizuin=3211828736; data_bizuin=3239826583; bizuin=3211828736; data_ticket=MY7BzVOs/eOR0o7KVMAz6kU7axsoln5E9yHzB8UFfr4OuWzLWc6wCq84S58drkZe; slave_sid=Nk9ibUw5QjVCT2czNFBEMDNyY3NVZlFIaEc0TjJ2SFdqVzhDaG9SNnpiZk5EMUJIOVNIeGRocUNiaFAyVFBqMWVfNWV4WVpwN0Z1aUk1WE43Y3UycUhBVm5ZYWM0UGhTWkVueFlFRk5PMTB2M0RPWlI2b0FRaVpCcEJYaW9Wcjd4TmluOGZwSVVDdnpkd0tE; slave_user=gh_2d4656f66685; xid=0c74682e70906d561039ca6e24d8ae8b; _clsk=o58sgn|1688813027677|1|1|mp.weixin.qq.com/weheat-agent/payload/record"

# 使用Cookie，跳过登陆操作

data = {
    "token": "20884314",
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": "0",
    "count": "5",
    "query": "",
    "fakeid": "这里进行替换",
    "type": "9",
}
headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Mobile Safari/537.36",

    }
content_json = requests.get(url, headers=headers, params=data).json()
count = int(content_json["app_msg_cnt"])
print(count)
page = int(math.ceil(count / 5))
print(page)
content_list = []
# 功能：爬取IP存入ip_list列表

for i in range(page):
    data["begin"] = i * 5
    user_agent = random.choice(user_agent_list)
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,

    }
    ip_headers = {
        'User-Agent': user_agent
    }
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        items = []
        items.append(item["title"])
        items.append(item["link"])
        t = time.localtime(item["create_time"])
        items.append(time.strftime("%Y-%m-%d %H:%M:%S", t))
        content_list.append(items)
    print(i)
    if (i > 0) and (i % 10 == 0):
        name = ['title', 'link', 'create_time']
        test = pd.DataFrame(columns=name, data=content_list)
        test.to_csv("url.csv", mode='a', encoding='utf-8')
        print("第" + str(i) + "次保存成功")
        content_list = []
        time.sleep(random.randint(60,90))
    else:
        time.sleep(random.randint(15,25))

name = ['title', 'link', 'create_time']
test = pd.DataFrame(columns=name, data=content_list)
test.to_csv("url.csv", mode='a', encoding='utf-8')
print("最后一次保存成功")