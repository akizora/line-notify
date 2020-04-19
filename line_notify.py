import requests
import feedparser
from time import sleep
import os

# RSSへアクセスし最新のURLを取得する
def getRssFeedData():
    # アクセスするrdfのURLを記載
    RSS_URL = 'https://www.mhlw.go.jp/stf/news.rdf'
    xml = feedparser.parse(RSS_URL)
    for entry in xml.entries:
        # linkの中からnewpageの最初のURLを取り出す
        if('newpage' in entry.link):
            print(entry.link)
            return entry.link

# LINEへ通知を行うメソッド
def lineNotifyTest(url):
    # 発行したトークンを記載します
    LINE_NOTIFY_TOKEN = '1234567890abcdefghijklmnopqrstuvwxyz'

    # LINE NotyfyのAPI URLを記載します
    LINE_NOTIFY_API = 'https://notify-api.line.me/api/notify'

    message = '\n厚生労働省からの最新情報があります。\n' + url
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN }

    # LINE通知を行う
    requests.post(LINE_NOTIFY_API, data=payload, headers=headers)

# URLが更新されたかチェック
def checkLatestNews():
    rss_url = getRssFeedData()
    path = './latest_url.txt'

    # latest_url.txtがなければ新規作成
    if not os.path.isfile(path):
        string = 'new file'
        with open(path, mode='w') as file:
            file.write(string)

    local_url = ''
    with open(path, mode='r') as file:
        local_url = file.read()

    # 新着情報があるかチェック
    if (local_url == rss_url):
        print('新着情報はありませんでした')
    else:
        print('testtest')
        lineNotifyTest(rss_url)
        with open(path, mode='w') as file:
            string = rss_url
            file.write(string)
        print('新着情報があったので通知しました')
    
while True:
    checkLatestNews()
    sleep(10)

