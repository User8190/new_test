import bs4
from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
import telebot
from telebot import types
# search
def search_engine(query):
    text = query+" site:baiscopelk.com OR site:cineru.lk OR site:piratelk.com 1..15"
    text = text.replace(" ","+")
    url = 'https://google.com/search?q=' + text
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text,"html.parser")
    heading_object = soup.find_all('div',{"class":"kCrYT"})
    titles = []
    link = []
    for info in heading_object:
        try:
            title = str(info.select("h3"))
            links = info.select("a")[0]['href']
            pure_link = links[links.index("https://"):links.index("&sa=U&")]

            if pure_link.count("/") ==4:
                new_title = title[title.index('AP7Wnd">') + 8:title.index('|')]
                link.append(pure_link)
                titles.append(new_title)
        except Exception as e:
            pass
    if not titles:
        return "Not Result"
    else:
        output = {"title": titles, 'link': link}
        return output


# zipdownloader
def download(url):
    r1 = requests.get(url)
    html_data = r1.text
    soup = bs(html_data, 'html.parser')

    def cineru():
        links = soup.select('a[data-link]')
        try:
            for i in links:
                lin = str(i)
                link = lin[lin.index('data-link="') + 11:lin.index('" href')]
                return link
        except Exception as e:
            print(e)
            return "error"

    def baiscopelk():
        links = soup.find_all("p", {"style": "padding: 0px; text-align: center;"})
        try:
            for i in links:
                lin = str(i)
                link = lin[lin.index('<a href="') + 9:lin.index('"><img ')]
                return link
        except Exception as e:
            print(e)
            return "error"

    def piratelk():
        links = soup.find_all("a", {"class": "aligncenter download-button"})
        try:
            for i in links:
                lin = str(i)
                link = lin[lin.index('href="') + 6:lin.index('" rel')]
                return link
        except Exception as e:
            print(e)
            return "error"

    sites = ["https://cineru.lk/", "https://www.baiscopelk.com/", "https://piratelk.com/"]
    if sites[0] in url:
        site_message = cineru()
    elif sites[1] in url:
        site_message = baiscopelk()
    else:
        site_message = piratelk()
    return site_message


#database
client = MongoClient("mongodb+srv://GavinduTharaka:Gavindu123@sinhalasubdownbot.1v9ix.mongodb.net/Bot?retryWrites"
                     "=true&w=majority")
db = client["Bot"]
users = db['All_users']
counts = db['counts']


def update_users(details):
    _id = details["_id"]
    try:
        username = details["username"]
        users.update_one({'_id': _id}, {"$set": {"username": "@" + str(username)}} )
        print("updated username")
    except Exception as e:
        print("Not UserName ", e)
        pass

    try:
        status = str(details['status'])
        print(status)
        users.update_one({'_id': _id},  {"$set": {'status' : status}})
        print("updated status")
    except Exception as e:
        print("Not Status ",e)
        pass


def insert_users(details):
    try:
        _id = details["_id"]
        username = details["username"]
        status = "active"
        users.insert_one({"_id": _id, "username": "@"+str(username), 'status': status})
    except:
        update_users(details)
        pass


def count_users():
    try:
        count = db.All_users.estimated_document_count()
        print(count)
        return count
    except Exception as e:
        print(e)
        pass


def delete_users():
    try:
        count = db.All_users.find({'status': 'delete'})
        return count
    except Exception as e:
        print(e)
        pass


def all_users():
    try:
        data = db.All_users.find()
        _id = []
        status = []
        username = []
        for i in data:
            _id.append(i["_id"])
            username.append(i["username"])
            status.append(i["status"])
        output = {"_id": _id, "username": username, "status": status}
        return output

    except:
        pass


def delete_user_count():
    count = 0
    for i in delete_users():
        count = count + 1
    return count


def active_user_count():
    try:
        data = db.All_users.find({'status': 'active'})
        count = 0
        for i in data:
            count = count + 1
        print()
        return count
    except Exception as e:
        print(e)
        pass


# keyboards
def start_key():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('SEND YOUR COMMENTS ✉')
    keyboard.row('SEARCH 🔎', 'UPDATES 📢')
    keyboard.row('RATE US ⭐')
    return keyboard


def cancel():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Cancel')
    return keyboard


def admin_key():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Send All',)
    return keyboard


def back_to_start():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Back to Start',)
    return keyboard


def invite_friends():
    url = "https://t.me/share/url?url=Film%20%E0%B6%91%E0%B6%9A%E0%B6%A7%20Tv%20series%20%E0%B6%91%E0%B6%9A%E0%B6%A7%20%20Sinhala%20subtitle%20%E0%B7%84%E0%B7%9C%E0%B6%BA%E0%B6%B1%E0%B7%80%E0%B7%8F%E0%B6%AF....%3F%F0%9F%99%82%0A%0A%F0%9F%94%B0Sinhala%20Sub%20Down%20Bot%F0%9F%94%B0%0A%20%20%E2%96%AA%EF%B8%8F%20Bot%20%E0%B6%91%E0%B6%9A%20Start%20%E0%B6%9A%E0%B6%BD%E0%B7%8F%0A%20%20%E2%96%AA%EF%B8%8F%20Search%20Button%20%E0%B6%91%E0%B6%9A%20click%20%E0%B6%9A%E0%B6%BD%E0%B7%8F%0A%20%20%E2%96%AA%EF%B8%8F%20Film%20%E0%B6%91%E0%B6%9A%E0%B7%9A%20%E0%B7%84%E0%B6%BB%E0%B7%92%20Tv%20series%20%E0%B6%B1%E0%B6%B8%20send%20%E0%B6%9A%E0%B6%BD%E0%B7%8F%0A%20%20%E2%96%AA%EF%B8%8F%20%E0%B6%B4%E0%B7%99%E0%B6%B1%E0%B7%8A%E0%B6%B1%E0%B6%B1%20results%20%E0%B7%80%E0%B6%BD%E0%B7%92%E0%B6%B1%E0%B7%8A%20subtitle%20%E0%B6%91%E0%B6%9A%20Download%20%E0%B6%9A%E0%B6%BD%E0%B7%8F%0A%0A18000%2B%20%E0%B6%AD%E0%B7%8A%20%E0%B7%80%E0%B7%90%E0%B6%A9%E0%B7%92%20Sinhala%20subtitle%20%E0%B6%B4%E0%B7%8A%E2%80%8D%E0%B6%BB%E0%B6%B8%E0%B7%8F%E0%B6%AB%E0%B6%BA%E0%B6%9A%E0%B7%92%E0%B6%B1%E0%B7%8A%20%E0%B6%85%E0%B7%80%E0%B7%81%E0%B7%8A%E2%80%8D%E0%B6%BA%20subtitle%20%E0%B6%91%E0%B6%9A%20%E0%B6%BD%E0%B7%9A%E0%B7%83%E0%B7%92%E0%B6%BA%E0%B7%99%E0%B6%B1%E0%B7%8A%E0%B6%B8%20%E0%B6%AD%E0%B7%9D%E0%B6%BB%E0%B7%8F%E0%B6%9C%E0%B6%B1%E0%B7%8A%E0%B6%B1.%E0%B6%B4%E0%B7%84%E0%B6%BD%20%E0%B6%BD%E0%B7%92%E0%B6%B1%E0%B7%8A%E0%B6%9A%E0%B7%8A%20%E0%B6%91%E0%B6%9A%20Click%20%E0%B6%9A%E0%B6%BB%E0%B6%BD%E0%B7%8F%20Sinhala%20Sub%20Down%20Bot%20%E0%B7%80%20Start%20%E0%B6%9A%E0%B6%BB%E0%B6%B1%E0%B7%8A%E0%B6%B1.%E0%B7%80%E0%B7%90%E0%B6%A9%E0%B7%9A%20%E0%B7%84%E0%B7%9C%E0%B6%AF%20%E0%B6%B1%E0%B6%B8%E0%B7%8A%20%E0%B6%BA%E0%B7%8F%E0%B7%85%E0%B7%94%E0%B7%80%E0%B6%B1%E0%B7%8A%E0%B6%A7%E0%B6%AD%E0%B7%8A%20Share%20%E0%B6%B4%E0%B7%8F%E0%B6%BB%E0%B6%9A%E0%B7%8A%20%E0%B6%AF%E0%B7%8F%E0%B6%B1%E0%B7%8A%E0%B6%B1.%F0%9F%94%A5%0A%0A%0Ahttps%3A%2F%2Ft.me%2Fsinhalasubdown_bot%0A"
    rate_url = "https://t.me/tlgrmcbot?start=sinhalasubdown_bot-review"
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button1 = types.InlineKeyboardButton(text="Share", url=str(url))
    button2 = types.InlineKeyboardButton(text="Rate us",url =str(rate_url) )
    keyboard.add(button1,button2)
    return keyboard


def rate_us():
    rate_url = "https://t.me/tlgrmcbot?start=sinhalasubdown_bot-review"
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button1 = types.InlineKeyboardButton(text="Share", url=str())
    button2 = types.InlineKeyboardButton(text="Rate us",url= rate_url)
    keyboard.add(button1,button2)
    return keyboard


# messages
start = "start message"
query_error = "*Something Wrong!*🚫 \n`Reported to admin`"
download_error = "*Can't Found This Subtitle.*⚠️\nplease try to download other"

rate = 'Type: Bot\n'\
        'Category: TV Series & Movies\n'\
        'Rating: ⭐️ 5.00 (3)\n'\
        'Language(s): English\n'\
        'Owner: Gavindu Tharaka\n\n'\
        'Menu URL: https://t.me/tlgrmcbot?start=sinhalasubdown_bot\n'\
        'Rating URL: https://t.me/tlgrmcbot?start=sinhalasubdown_bot-review\n'

admin_start_message = "*This message show only Admins*\n▪️ /admin\_on - Turn on Admin mode\n▪️ /admin\_off - Turn off Admin mode"
