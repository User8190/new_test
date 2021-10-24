import time
import telebot
from telebot import types
from bs4 import BeautifulSoup as bs4
import requests
TOKEN = "2009079618:AAEGX3cvXmhCaJuVj4wWwZc8fA88u_N9br0"
bot = telebot.TeleBot(TOKEN)

admin_chat_id = 1376213565
output_data = ""


#search
def download(url):
    r1 = requests.get(url)
    html_data = r1.text
    soup = bs4(html_data, 'html.parser')

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


# zipdownloader
def download(url):
    r1 = requests.get(url)
    html_data = r1.text
    soup = bs4(html_data, 'html.parser')

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


# Database
from pymongo import MongoClient
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


# send admin
def send_to_admin(message):
    try:
        bot.send_message(admin_chat_id, message,parse_mode='Markdown')
    except Exception as e:
        print("Bot admin chat id is wrong")
        print(e)
        pass


def download_count(n=0):
    # Update After
    pass


def users(dic=None):
    if dic is None:
        return count_users()
    else:
        return insert_users(dic)


@bot.message_handler(commands=["start"])
def welcome(message):
    global output_data
    bot.send_message(message.chat.id,start,reply_markup=start_key())
    bot.send_message(message.chat.id,"*Invite Your Friends*",reply_markup=invite_friends(),parse_mode="Markdown")
    dic = {'_id': int(message.from_user.id), 'username': str(message.from_user.username)}
    users(dic)
    output_data = ""
    if message.chat.id == admin_chat_id:
        bot.send_message(admin_chat_id,admin_start_message,parse_mode="Markdown")


@bot.message_handler(commands=["send_to_admin"])
def send_admin_(message):
    global output_data
    msg = "*Send your comment💬*"
    bot.send_message(message.chat.id,msg,parse_mode="Markdown")
    output_data = "send_to_admin"


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    global output_data
    global titles
    global urls
    if output_data == "send_to_admin" and str(message.text)!="Cancel":
        message_from_user = str(message.text)
        msg = "*from user*\nchat id : `"+str(message.from_user.id)+"`\nmessage : "+message_from_user
        send_to_admin(msg)
        bot.send_message(message.chat.id,"*Comment was sent to admin Successfully✅*", parse_mode="Markdown",reply_markup=back_to_start())
        output_data = ""

    elif str(message.text)=="SEARCH 🔎":
        bot.send_message(message.chat.id, "Send *Film* or *TV Show* name🎞",parse_mode="Markdown", reply_markup=cancel())
        output_data = "search"

    elif str(message.text) == "Cancel" or str(message.text)=='Back to Start':
        bot.send_message(message.chat.id, start, reply_markup=start_key())
        output_data = ""
        dic = {'id': int(message.from_user.id), 'username': str(message.from_user.username)}
        users(dic)
    elif str(message.text) =="":
        pass
    elif output_data == "search":
        keyboardmain = types.InlineKeyboardMarkup(row_width=4)
        name = str(message.text)
        movie = search_engine(name)
        if movie != "Not Result":
            urls = movie['link']
            titles = movie["title"]
            for i in range(len(titles)):
                button = types.InlineKeyboardButton(text=titles[i], callback_data=str(i))
                keyboardmain.add(button)
            bot.send_message(message.chat.id,"*Result Found 🎬*\n` Search  : "+str(message.text)+"\n Results : "+str(len(titles))+"`\n\n*▪️Click and Download▪️*",reply_markup=keyboardmain, parse_mode= 'Markdown')
            return titles
        else:
            msg = "*Sorry⚠️*\nYour search result not found!"
            bot.send_message(message.chat.id,msg,parse_mode='Markdown')

            bot.send_message(message.chat.id, "Please *Cancel search* or Send *other name*", parse_mode='Markdown')
            output_data = "search"
    elif str(message.text)=='SEND YOUR COMMENTS ✉':
        msg = "*Send your comment💬*"
        bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=cancel())
        output_data = "send_to_admin"
        return output_data
    elif str(message.text) == 'RATE US ⭐':
        bot.send_message(message.chat.id, rate, reply_markup=back_to_start())


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    global urls
    message = str(call.data)
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    if message in numbers:
        try:
            n = int(message)
            url = zipdownloader.download(urls[n])
            if url is not None:
                download_count()
                caption = "*Download from SinhalaSubDown Bot*😋\n"
                bot.send_document(call.message.chat.id, url, caption=caption, parse_mode="Markdown")
            else:
                msg = download_error
                bot.send_message(call.message.chat.id,msg,parse_mode="Markdown")
        except Exception as e:
            msg = query_error
            bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
            send_to_admin(str(e)+str(" (if message in numbers)"))


bot.polling()
