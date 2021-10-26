import bs4
from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
import telebot
from telebot import types
import rarfile
from zipfile import ZipFile
import os

# search


# search engine
def did_you(query, other=""):
    text = query+other
    text = text.replace(" ", "+")
    url = 'https://google.com/search?q=' + text
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    did_you_ = ""
    try:
        did_you_ = soup.find('div', {'class': 'MUxGbd v0nnCb lyLwlc'})
        did_you_ = str(did_you_.getText().replace(other, ""))
        did_you_ = did_you_.replace(":https://www.imdb.com/title", "")
    except Exception as e:
        pass
    if did_you_ is None:
        search = query
    else:
        search = did_you_
        search = search.replace("Did you mean: ", "").replace("Showing results for ", "")
    return search


def baiscopelk_search(search):
    baiscopelk_url = "https://www.baiscopelk.com/?s="
    url = baiscopelk_url+search
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    site_items = soup.find_all('h2',{"class":"post-box-title"})
    links = []
    titles = []
    for x in range(len(site_items)):
        if "mega-menu-link" in str(site_items[x]) or "rel=\"bookmark\"" in str(site_items[x]) or "ttip" in str(site_items[x]):
            pass
        else:
            htmldata = str(site_items[x])
            page_soup1 = bs4.BeautifulSoup(htmldata, "html.parser")
            hreflink = page_soup1.findAll('a')
            if len(hreflink) != 0:
                for key in search.split():
                    if key in str(hreflink[0].getText().lower()):
                        title = hreflink[0].getText()
                        try:
                            ne_title = title[:title.index(" | ")]
                        except:
                            ne_title = title
                        if ne_title not in titles:
                            titles.append(ne_title)
                            links.append(hreflink[0]['href'])
    return {"title": titles, 'link': links}


def pirate_search(search):
    pirate_url = "https://piratelk.com/?s="
    url = pirate_url+search
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    site_items = soup.find_all('h2',{"class":"post-box-title"})

    links = []
    titles = []
    for x in range(len(site_items)):
        htmldata = str(site_items[x])
        page_soup1 = bs4.BeautifulSoup(htmldata, "html.parser")
        hreflink = page_soup1.findAll('a')
        if len(hreflink) != 0:
            for key in search.split():
                if key in str(hreflink[0].getText().lower()):
                    title = hreflink[0].getText()
                    try:
                        ne_title = title[:title.index(" | ")]
                    except:
                        ne_title = title
                    if ne_title not in titles:
                        titles.append(ne_title)
                        links.append(hreflink[0]['href'])
    return {"title": titles, 'link': links}


def cineru_search(search):
    cineru_url = "https://cineru.lk/?s="
    url = cineru_url+search
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    site_items = soup.find_all('h2',{"class":"post-box-title"})

    links = []
    titles = []
    for x in range(len(site_items)):
        htmldata = str(site_items[x])
        page_soup1 = bs4.BeautifulSoup(htmldata, "html.parser")
        hreflink = page_soup1.findAll('a')
        if len(hreflink) != 0:
            for key in search.split():
                if key in str(hreflink[0].getText().lower()):
                    title = hreflink[0].getText()
                    try:
                        ne_title = title[:title.index(" | ")]
                    except:
                        ne_title = title
                    if ne_title not in titles:
                        titles.append(ne_title)
                        links.append(hreflink[0]['href'])
    return {"title": titles, 'link': links}


def search_engine(search):
    search = search.lower()
    search = did_you(search," subtitles")
    search = search.replace("("," ").replace(")"," ")
    baiscopelk = baiscopelk_search(search)
    pirate = pirate_search(search)
    cineru = cineru_search(search)
    if len(baiscopelk['title'])>3:
        return baiscopelk
    elif len(pirate['title'])>3:
        return pirate
    elif len(cineru['title'])>3:
        return cineru
    else:
        new_title = baiscopelk['title']+pirate['title']+cineru['title']
        new_link = baiscopelk['link'] + pirate['link'] + cineru['link']
        if len(new_title)>0:
            return  {'title': new_title, 'link': new_link}
        else:
            return "Not Result"

# zipdownloader
def download(url,path):
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
    r3 = requests.get(site_message)

    if r3.status_code == 200:
        if "rar" in site_message:
            sv = path+"download_from_@sinhalasubdown_bot.rar"
        else:
            sv = path+"download_from_@sinhalasubdown_bot.zip"
        file = open(sv, "wb")
        file.write(r3.content)
        file.close()
        print("File download success !")
        return unzip(sv,path)


# database
client = MongoClient("mongodb+srv://GavinduTharaka:Gavindu123@sinhalasubdownbot.1v9ix.mongodb.net/Bot?retryWrites"
                     "=true&w=majority")
db = client["Bot"]
users = db['All_users']
counts = db['counts']


def all_user_details():
    user_list = []
    for i in users.find():
        user_list.append(i)
    return user_list


def update_users(details):
    _id = details["_id"]
    try:
        username = details["username"]
        users.update_one({'_id': _id}, {"$set": {"username": "@" + str(username)}} )
    except Exception as e:
        pass

    try:
        status = str(details['status'])
        users.update_one({'_id': _id},  {"$set": {'status' : status}})
    except Exception as e:
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
        name = []
        for i in data:
            _id.append(i["_id"])
            username.append(i["username"])
            status.append(i["status"])
            name.append(i['name'])
        output = {"_id": _id, "username": username, "status": status, 'name': name}
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


def user_info_database(user_id):
    user = db.All_users.find({"_id": user_id})
    for us in user:
        return us
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


def join_channel():
    channel_url = "https://t.me/SinhalaSubDown"
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button2 = types.InlineKeyboardButton(text="Join",url= channel_url)
    keyboard.add(button2)
    return keyboard


def user_info():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    button1 = types.InlineKeyboardButton(text="Send Message", callback_data="send_message")
    button2 = types.InlineKeyboardButton(text="User Downloads", callback_data="downloads")
    button3 = types.InlineKeyboardButton(text="Messages",callback_data="messages")
    keyboard.add(button1,button2)
    keyboard.add(button3)
    return keyboard

# messages
def start(name):
    start = "Hi %s ,\n*I am Sinhala Sub Down Bot(Beta)🤖*\n\n*උපදෙස් ℹ *\n*🔹 SEARCH 🔎* බට්න් එක ක්ලික් කරලා subtitles ඕන කරන film එකේ හෝ TV series එකේ නම මැසේජ් කරන්න.\n🔹 හරිම search result එක ගන්න ඕන නිසා filter ගොඩක් දාලා තියෙයි. ඒක නිසා සමහර sub හොයන්න ටිකක් වැඩි පුර කාලය වැය වෙයි." \
            "\n🔹 අදහස් යෝජනා චෝදනා එහෙම තියේ නම් *SEND YOUR COMMENTS ✉* බටන් එක ක්ලික් කරලා එවන්න පුලුවන්.\n🔹 තව දින කීපයකින් කලින් බොට්ට මේ update එක දෙනවා. ඊට පස්සේ මේක වැඩ කරන්නෙ නෑ."%name
    return start
query_error = "*Something Wrong!*🚫 \n`Reported to admin`"
download_error = "*Can't Found This Subtitle.*⚠️\nplease try to download other"

rate = 'Type: Bot\n'\
        'Category: TV Series & Movies\n'\
        'Rating: ⭐️ 5.00 (3)\n'\
        'Language(s): English\n'\
        'Owner: Gavindu Tharaka\n\n'\
        'Menu URL: https://t.me/tlgrmcbot?start=sinhalasubdown_bot\n'\
        'Rating URL: https://t.me/tlgrmcbot?start=sinhalasubdown_bot-review\n'

admin_start_message = "*This message show only Admins*\n▪️ /admin\_on - Turn on Admin mode"

admin_commands ="*Admin Commands*\n/send\_all - Share messages with all users\n/user\_list - To get all users name and chat id\n" \
                "/user <user id> - To send privet message and get other details"


# Unzip
def unzip(file_path,path):
    if '.rar' in file_path:
        r = rarfile.RarFile(file_path)
        r.extract(path=path)
        r.close()
    elif '.zip' in file_path:
        z = ZipFile(file_path, 'r')
        z.extractall(path=path)
        z.close()
    file_list = []
    for path, subdirs, files in os.walk("downloads/"):
        for name in files:
            file = str(os.path.join(path, name))
            file = file.replace("\\","/")
            if ".zip" not in file and ".htm" not in file and ".html" not in file and ".txt" not in file:
                file_list.append(file)
    return file_list


def send(userid, message, bot, type = None):
    caption = ""
    if str(message.caption) is not None:
        caption = ""
    if message.content_type == "text":
        en = message.entities
        bot.send_message(userid, message.text, entities=en)
    else:
        en = message.caption_entities
        try:
            bot.send_photo(userid, message.photo[0].file_id, caption, caption_entities=en)
        except Exception as e:
            try:
                bot.send_document(userid, message.document.file_id, caption=caption, caption_entities=en)
            except Exception as e:
                try:
                    bot.send_video(userid, message.video.file_id, caption=caption, caption_entities=en)
                except Exception as e:
                    try:
                        bot.forward_message(userid, message.chat.id, message.id)
                    except:
                        return "error"

"""for user in db.All_users.find():
    _id = user['_id']
    users.update_one({'_id': _id}, {"$set": {"name": "Name"}})
    users.update_one({'_id': _id}, {"$set": {"down_count": "D Count"}})
    users.update_one({'_id': _id}, {"$set": {"last_seen": "Last seen"}})
print("update finished")
"""
