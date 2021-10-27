import time
import os
import telebot
from telebot import types
import shutil
import os
import stat


TOKEN = "2019524542:AAFJuxb__HD8_CSuoPhjOpsjllikEw-Btfc"
bot = telebot.TeleBot(TOKEN)

admin_chat_id = 1376213565
output_data = ""
share_with_all = ""
send_user = ""
user_chat_id = ""

# send users
def send_to_users(message):
    global send_user
    global user_chat_id
    from _functions import send
    try:
        if send_user == 1 and message.chat.id == admin_chat_id:
            bot.send_message(user_chat_id,"*[Private message from Admin]*",parse_mode="Markdown")
            send(user_chat_id,message,bot)
    except:
        pass


def send_all_u(message):
    from _functions import all_user_details
    from _functions import send,update_users
    all_count_users = 0
    deleted_users = 0
    if message.chat.id == admin_chat_id:
        for i in all_user_details():
            all_count_users = all_count_users +1
            _id = i['_id']
            details = {'_id': _id, 'status': "active"}
            try:
                if send(_id,message,bot) == 'error':
                    deleted_users = deleted_users +1
                    details = {'_id': _id, 'status': "delete"}
                update_users(details)
            except:
                pass
        bot.send_message(admin_chat_id,"*All users :* "+str(all_count_users)+"\n*Deleted users :* "+str(deleted_users)+"\n\n*"+str(all_count_users -deleted_users)+" users are active now*")


# send admin
def send_to_admin(message):
    try:
        bot.send_message(admin_chat_id, message, parse_mode='Markdown')

    except Exception as e:
        print("Bot admin chat id is wrong")
        print(e)
        pass


def download_count(n=0):
    # Update After
    pass


def users(dic=None):
    from _functions import count_users, insert_users
    if dic is None:
        return count_users()
    else:
        return insert_users(dic)


@bot.message_handler(commands=["start"])
def welcome(message):
    from _functions import start_key, invite_friends, start, admin_start_message
    global output_data
    name = message.from_user.first_name
    bot.send_message(message.chat.id, start(name), reply_markup=start_key(), parse_mode="Markdown")
    bot.send_message(message.chat.id, "*යාලුවන්ටත් ඉන්වයිට් පාරක් දාන්න. හොද නරක කියලා rate එකකුත් දාන්න*☺️",
                     reply_markup=invite_friends(), parse_mode="Markdown")
    dic = {'_id': int(message.from_user.id), 'username': str(message.from_user.username)}
    users(dic)
    output_data = ""
    print(name, "Start the Bot")
    if message.chat.id == admin_chat_id:
        bot.send_message(admin_chat_id, admin_start_message, parse_mode="Markdown")
    else:
        bot.send_message(admin_chat_id, "*" + str(name) + "* is started Bot", parse_mode="Markdown")


@bot.message_handler(commands=["send_all"])
def send_admin_all(message):
    if message.chat.id == admin_chat_id:
        global share_with_all
        bot.send_message(admin_chat_id, "*Send Message for need to share with all users*", parse_mode="Markdown")
        share_with_all = 1


@bot.message_handler(commands=["admin"])
def send_admin_(message):
    if message.chat.id == admin_chat_id:
        from _functions import admin_commands
        msg = admin_commands
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id,"*You are not an admin*",parse_mode="Markdown")


@bot.message_handler(commands=["user_list"])
def send_admin_(message):
    if message.chat.id == admin_chat_id:
        from _functions import all_users
        user_list = all_users()
        msg = ""
        x = 0
        for i in range(len(user_list['_id'])):
            num = i +1
            li = "["+str(num)+"] "+str(user_list['name'][i])+' '+str(user_list['username'][i])+' ID : '+str(user_list['_id'][i])+'\n'
            if x == 9:
                try:
                    bot.send_message(message.chat.id, msg)
                except Exception as e:
                    print(e)
                msg = ''
                x = 0
            else:
                x+=1
            msg = msg+li

        try:
            bot.send_message(message.chat.id, msg)
        except Exception as e:
            print(e)
    else:
        bot.send_message(message.chat.id,"*You are not an admin*",parse_mode="Markdown")


@bot.message_handler(commands=["user"])
def user_details(message):
    if message.chat.id == admin_chat_id:
        global user_chat_id
        user_id = str(message.text)
        user_id = user_id.replace("/user", "")
        if user_id == "":
            bot.send_message(admin_chat_id, "*Sorry this command is working with user id*", parse_mode="Markdown")
        else:
            from _functions import user_info, user_info_database
            try:
                user = user_info_database(int(user_id))
                name = user["name"]
                user_name = str(user["username"]).replace("_", "\_")
                totdown = str(user["down_count"]).replace("_", "\_")
                last_seen = str(user["last_seen"]).replace("_", "\_")
                msg = "*Users Info*\n*▪️Name* : " + str(name) + "\n*▪️User name* :" + str(
                    user_name) + "\n*▪️Total downloads* : " + str(totdown, ) + "\n*▪️Last seen* : " + str(last_seen)
                bot.send_message(admin_chat_id, msg, parse_mode="Markdown", reply_markup=user_info())
                user_chat_id = user["_id"]

            except Exception as e:
                bot.send_message(message.chat.id,"Wrong chat id",parse_mode="Markdown")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.get_chat_member(message.chat.id,message.from_user.id)
    from _functions import start, rate
    from _functions import start_key, back_to_start, cancel
    global send_user
    global user_chat_id
    global output_data
    global titles
    global urls
    print(message)
    if output_data == "send_to_admin" and str(message.text) != "Cancel":
        message_from_user = str(message.text)
        msg = "*from user*\nchat id : `" + str(message.from_user.id) + "`\nmessage : " + message_from_user
        send_to_admin(msg)
        bot.send_message(message.chat.id, "*Comment was sent to admin Successfully✅*", parse_mode="Markdown",
                         reply_markup=back_to_start())
        output_data = ""

    elif str(message.text) == "SEARCH 🔎":
        bot.send_message(message.chat.id, "Send *Film* or *TV Show* name🎞", parse_mode="Markdown",
                         reply_markup=cancel())
        output_data = "search"

    elif str(message.text) == "Cancel" or str(message.text) == 'Back to Start':
        name = message.from_user.first_name
        bot.send_message(message.chat.id, start(name), reply_markup=start_key(), parse_mode="Markdown")
        output_data = ""
        dic = {'_id': int(message.from_user.id), 'username': str(message.from_user.username)}
        users(dic)
    elif str(message.text) == "UPDATES 📢":
        from _functions import join_channel
        bot.send_message(message.chat.id, "*අපේ Telegram channel එකටත් ජොයින් වෙන්න*", reply_markup=back_to_start(),
                         parse_mode="Markdown")
        bot.send_message(message.chat.id, "*Join Telegram channel*", reply_markup=join_channel()
                         , parse_mode="Markdown")
    elif output_data == "search":
        bot.send_message(message.chat.id, "*Please Wait! ⏰*\nSearching subtitles for : *" + str(message.text) + "*",
                         parse_mode="Markdown")
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
            bot.send_message(message.chat.id,
                             "*Result Found 🎬*\n` Search  : " + str(message.text) + "\n Results : " + str(
                                 len(titles)) + "`\n\n*▪️Click and Download▪️*", reply_markup=keyboardmain,
                             parse_mode='Markdown')
            return titles
        else:
            msg = "*Sorry⚠️*\nYour search result not found!"
            bot.send_message(message.chat.id, msg, parse_mode='Markdown')

            bot.send_message(message.chat.id, "Please *Cancel search* or Send *other name*", parse_mode='Markdown')
            output_data = "search"
    elif str(message.text) == 'SEND YOUR COMMENTS ✉':
        msg = "*Send your comment💬*"
        bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=cancel())
        output_data = "send_to_admin"
        return output_data
    elif str(message.text) == 'RATE US ⭐':
        bot.send_message(message.chat.id, rate, reply_markup=back_to_start())

    elif send_user == 1 and message.chat.id == admin_chat_id:
        send_to_users(message)
    elif share_with_all == 1:
        send_all_u(message)


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):  # <- passes a CallbackQuery type object to your function
    global urls
    from _functions import download_error, query_error
    message = str(call.data)
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
               '19', '20']
    if message in numbers:
        user_folder_name = 'downloads/'+str(call.message.chat.id)+"/"
        try:
            from _functions import download
            n = int(message)
            urls = urls
            url = download(urls[n],user_folder_name)
            print(url)
            if url is not None:
                bot.send_document(call.message.chat.id, url["file"], caption='\nThis File Download from sinhalasubdown_bot')
                download_count()
                try:
                    url["file"].close()
                    os.remove(url['name'])
                    print("file deleted")
                except:
                    print("file not found")

            else:
                msg = download_error
                bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
        except NameError:
            from _functions import back_to_start
            bot.send_message(call.message.chat.id,
                             "*Subtitle searching session is expired⚠️*\nClick *Back to start* and search again",
                             parse_mode="Markdown", reply_markup=back_to_start())

        except Exception as e:
            print(e)
            from _functions import back_to_start
            erro_ = str(e)
            erro_ = erro_.replace("_", "\_")
            msg = query_error
            bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
            bot.send_message(call.message.chat.id, "Click *Back to start* and search again", parse_mode="Markdown",
                             reply_markup=back_to_start())
            send_to_admin(str(erro_) + str(" (if message in numbers)"))
    global send_user
    try:
        if user_chat_id is not None and call.data == "send_message":
            bot.send_message(admin_chat_id," Send a Message",parse_mode="Markdown")
            send_user = 1
    except Exception as e:
        print(e)
        pass


@bot.message_handler(content_types=["photo",'video','document'])
def media(message):
    if share_with_all == 1 and message.chat.id == admin_chat_id:
        send_all_u(message)
    elif message.chat.id == admin_chat_id:
        send_to_users(message)





def principal():
    while True:
        try:
            bot.polling(True)
            bot.polling(none_stop=True)
        except:
            time.sleep(10)

principal()
