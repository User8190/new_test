import time
import telebot
from telebot import types

TOKEN = "2009079618:AAEGX3cvXmhCaJuVj4wWwZc8fA88u_N9br0"
bot = telebot.TeleBot(TOKEN)

admin_chat_id = 1376213565
output_data = ""



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
    from _functions import count_users,insert_users
    if dic is None:
        return count_users()
    else:
        return insert_users(dic)


@bot.message_handler(commands=["start"])
def welcome(message):
    from _functions import start_key,invite_friends,start,admin_start_message
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
    from _functions import start,rate
    from _functions import start_key, back_to_start,cancel
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
        dic = {'_id': int(message.from_user.id), 'username': str(message.from_user.username)}
        users(dic)
    elif str(message.text) =="":
        pass
    elif output_data == "search":
        keyboardmain = types.InlineKeyboardMarkup(row_width=4)
        name = str(message.text)
        from _functions import search_engine
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
    from _functions import download_error,query_error
    message = str(call.data)
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    if message in numbers:
        try:
            from _functions import download
            n = int(message)
            url = download(urls[n])
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
