import config
import ship_i18n
import emailSend
import httpx
import datetime
import re
from urllib.parse import quote


class Requests:
    # 定义POST请求函数
    @staticmethod
    def post(url: str, headers=None, params=None, data=None, json_boby=None):
        while True:
            try:
                response = httpx.post(url=url, headers=headers, params=params, data=data, json=json_boby, timeout=60)
                break
            except Exception as error:
                print(f"请求错误：{error}")
        return response

    # 定义GET请求函数
    @staticmethod
    def get(url: str, headers=None, params=None):
        while True:
            try:
                response = httpx.get(url=url, headers=headers, params=params, timeout=60)
                break
            except Exception as error:
                print(f"请求错误：{error} {url}")
        return response


# 实例化请求类
pool = Requests()


# 定义获取飞船列表请求函数
def get_id_list(cookie):
    url = 'https://robertsspaceindustries.com/pledge-store/api/upgrade/graphql'
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "cookie": cookie,
        "origin": "https://robertsspaceindustries.com",
        "pragma": "no-cache",
        "referer": "https://robertsspaceindustries.com/pledge",
        "sec-ch-ua": "\"Chromium\";v=\"9\", \"Not?A_Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/10",
        # "x-csrf-token": "e87fb608196b22009f3349e597ca5e45686fe779fdbd9d72ce461c7c1eb6dd8c"
    }
    data = [{
        "operationName": "filterShips",
        "variables": {
            "fromFilters": [],
            "toFilters": []
        },
        "query": "query filterShips($fromId: Int, $toId: Int, $fromFilters: [FilterConstraintValues], $toFilters: [FilterConstraintValues]) {\n  from(to: $toId, filters: $fromFilters) {\n    ships {\n      id\n    }\n  }\n  to(from: $fromId, filters: $toFilters) {\n    featured {\n      reason\n      style\n      tagLabel\n      tagStyle\n      footNotes\n      shipId\n    }\n    ships {\n      id\n      skus {\n        id\n        price\n        upgradePrice\n        unlimitedStock\n        showStock\n        available\n        availableStock\n      }\n    }\n  }\n}\n"
    }]
    response = pool.post(url=url, headers=headers, json_boby=data)
    ship_id_json = response.json()
    # print(ship_id_json)
    return ship_id_json


# 定义获取飞船ID列表请求函数
def get_ship_list(cookie):
    url = 'https://robertsspaceindustries.com/pledge-store/api/upgrade/graphql'
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "cookie": cookie,
        "origin": "https://robertsspaceindustries.com",
        "pragma": "no-cache",
        "referer": "https://robertsspaceindustries.com/pledge",
        "sec-ch-ua": "\"Chromium\";v=\"9\", \"Not?A_Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/10",
        # "x-csrf-token": "e87fb608196b22009f3349e597ca5e45686fe779fdbd9d72ce461c7c1eb6dd8c"
    }
    data = [
        {
            "operationName": "initShipUpgrade",
            "variables": {},
            "query": "query initShipUpgrade {\n  ships {\n    id\n    name\n    medias {\n      productThumbMediumAndSmall\n      slideShow\n    }\n    manufacturer {\n      id\n      name\n    }\n    focus\n    type\n    flyableStatus\n    owned\n    msrp\n    link\n    skus {\n      id\n      title\n      available\n      price\n      body\n      unlimitedStock\n      availableStock\n    }\n  }\n  manufacturers {\n    id\n    name\n  }\n  app {\n    version\n    env\n    cookieName\n    sentryDSN\n    pricing {\n      currencyCode\n      currencySymbol\n      exchangeRate\n      taxRate\n      isTaxInclusive\n    }\n    mode\n    isAnonymous\n    buyback {\n      credit\n    }\n  }\n}\n"
        }
    ]
    response = pool.post(url=url, headers=headers, json_boby=data)
    ship_json = response.json()
    # print(cookie)
    # print(idJson)
    return ship_json


# 定义获取商店数据
def get_pledge_data():
    url = 'https://robertsspaceindustries.com/en/pledge'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"9\", \"Not?A_Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/10"
    }
    response = pool.get(url=url, headers=headers)
    xsrf_token = re.findall("'name' : 'Rsi-XSRF', 'token' : '(.*?)', 'ttl' : ", response.text)[0]
    # print(xsrf_token)
    response_cookie = response.cookies.get('Rsi-Token')
    # print(response_cookie)
    auth_data = {
        "Rsi-Token": response_cookie,
        "Rsi-XSRF": quote(
            f"{xsrf_token}nclaYcvJB3C4f%2BkX0RXwpg:{int((datetime.datetime.now() + datetime.timedelta(minutes=+30)).timestamp() * 1000)}"),
    }
    # print(auth_data)
    response_cookie = get_token(auth_data)
    xsrf_token = get_context(auth_data)
    response_cookie.update(xsrf_token)
    return response_cookie


# 获取Token的请求函数
def get_token(auth_data):
    url = 'https://robertsspaceindustries.com/api/account/v2/setAuthToken'
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "cookie": f"{'; '.join([k + '=' + v for k, v in auth_data.items()])}",
        "origin": "https://robertsspaceindustries.com",
        "pragma": "no-cache",
        "referer": "https://robertsspaceindustries.com/pledge",
        "sec-ch-ua": "\"Chromium\";v=\"9\", \"Not?A_Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/10",
        "x-rsi-token": f"{auth_data.get('Rsi-Token')}"
    }
    response = pool.post(url=url, headers=headers, json_boby={})
    rsi_auth = response.cookies.get('Rsi-Account-Auth')
    # print(rsi_auth)
    rsi_params = {"Rsi-Account-Auth": rsi_auth}
    rsi_params.update(auth_data)
    return rsi_params


# 定义获取Context的请求函数
def get_context(auth_data):
    url = 'https://robertsspaceindustries.com/api/ship-upgrades/setContextToken'
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "cookie": f"{'; '.join([k + '=' + v for k, v in auth_data.items()])}",
        "origin": "https://robertsspaceindustries.com",
        "pragma": "no-cache",
        "referer": "https://robertsspaceindustries.com/pledge",
        "sec-ch-ua": "\"Chromium\";v=\"9\", \"Not?A_Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/10",
        "x-rsi-token": f"{auth_data.get('Rsi-Token')}"
    }
    data = {
        "fromShipId": None,
        "toShipId": None,
        "toSkuId": None,
        "pledgeId": None
    }
    res = pool.post(url=url, headers=headers, json_boby=data)
    context = res.cookies.get('Rsi-ShipUpgrades-Context')
    # print(Context)
    params = {"Rsi-ShipUpgrades-Context": context}
    params.update(auth_data)
    return params


# 定义处理抓包返回值函数
def process_ship_data(params_ship_list, params_id_list):
    ship_list = params_ship_list[0]['data']['ships']
    id_list = params_id_list[0]['data']['to']['ships']

    wb_ships = []

    for s_list in ship_list:
        # print(f'"{s_list['name']}":"{s_list['name']}",')
        for s_id in id_list:
            if s_list['id'] == s_id['id']:
                if len(s_id['skus']) > 1:
                    original_price = s_id['skus'][1]['price'] // 100
                    wb_price = s_id['skus'][0]['price'] // 100
                    ship_name = ship_i18n.i18n.get(s_list['name'], s_list['name'])
                    # 抓取飞船缩略图，价格，名字等信息
                    wb_ships.append({'img': s_list['medias']['productThumbMediumAndSmall'], 'name': ship_name,
                                     'original_price': original_price, 'wb_price': wb_price,
                                     'saving_price': original_price - wb_price})
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"当前时间：{current_time}")
    if len(wb_ships) > 0:
        print("当前正在售卖的WB CCU：")
        for wb in wb_ships:
            print(
                f" {wb['name']}\n  {wb['original_price']} - {wb['wb_price']} = {wb['original_price'] - wb['wb_price']} $")

        # 邮件发送
        from_email = config.from_email
        smtp_server = config.smtp_server
        smtp_port = config.smtp_port
        login = config.login
        password = config.password

        subject = config.title
        for email in config.to_email:
            to_email = email
            html_body = config.body
            for ship in wb_ships:
                html_body += f'<div class="div"><img src="{ship["img"]}"><span class="name">{ship["name"]}</span><span>&nbsp;{ship["original_price"]}&nbsp;-&nbsp;{ship["wb_price"]}&nbsp;=&nbsp;{ship["saving_price"]}$</span></div>'
            html_body += "</body></html>"

            emailSend.send_email(subject, html_body, to_email, from_email, smtp_server, smtp_port, login, password)
    else:
        print("今日暂无WB CCU")


# 启动函数
def start_get_wbccu():
    cookie = '; '.join([k + '=' + v for k, v in get_pledge_data().items()])
    process_ship_data(get_ship_list(cookie), get_id_list(cookie))
