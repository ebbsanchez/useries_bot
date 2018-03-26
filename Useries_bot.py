# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import os


TOKEN = os.environ["USERIES_BOT_TOKEN"]


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
root = 'https://next-episode.net'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def get_flash_date():
    flash_url = 'https://next-episode.net/the-flash'    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    r = requests.get(flash_url,headers=headers) # 讀取網址
    soup = BeautifulSoup(''.join(r.text),'lxml')       # 讀進BeautifulSoup
    
    return date

def flash_date(bot,update):
    date = get_flash_date()
    bot.send_message(chat_id=update.message.chat_id, text="Next episode of The Flash: {}".format(date))


def search(search_keyword):

    search_url = 'https://next-episode.net/site-search-{}.html'.format(search_keyword)
    skip_search = 0
    
    r = requests.get(search_url,headers=headers) # 讀取網址
    soup = BeautifulSoup(''.join(r.text),'lxml')       # 讀進BeautifulSoup
    # results = soup.find_all('div',class_='list_item') # 取得所有搜尋結果
    result = soup.find('div',class_='list_item') #取得第一筆搜尋節果
    if result is not None:
        result_url = result.find('span').find('a')['href']
        result_url = root + result_url
    elif soup.find(id='show_name'):
        result_url = search_url
        skip_search = 1
    else:
        return "oops! 從關鍵字「{}」找不到任何美劇...".format(search_keyword)
    if skip_search == 0:
        r = requests.get(result_url,headers=headers)
    soup = BeautifulSoup(''.join(r.text), 'lxml')
    nextep_block = soup.body.find_all('div', id="next_episode")
    if len(nextep_block) == 0:
        return "Oops! " + soup.title.text[:-15] + " 已經播完了！ "
    elif 'no info' in str(nextep_block[0]):
        return "很可惜....目前尚未有「{}」下一集的消息....".format(soup.title.text[:-15])
    else:
        nextep_block = nextep_block[0]

    date = nextep_block.text.split('Date:')[1].split('\t')[0]
    result ="「" + soup.title.text[:-15] +"」的下一集撥出時間是： " + date
    
    return result


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=search(update.message.text))


from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
flash_handler = CommandHandler('flash', flash_date)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(flash_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()