import telebot
from telebot import types


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
