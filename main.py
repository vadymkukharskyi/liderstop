import sqlite3
import telebot
import top
from telebot import types

bot = telebot.TeleBot('5129962077:AAFVambFD9rjyDrU6ZsNbXmBfO9XJPTOzuI')


@bot.message_handler(commands=["start"])
def start_command_handler(msg):
    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    if " " in msg.text:
        referrer_candidate = msg.text.split()[1]
        if referrer_candidate == str(user_id):
            bot.send_message(msg.chat.id, "ℹ️Вы не можете пригласить сами себя.")
            goin(user_id, None, first_name)
        else:
            if boolbot(user_id):
                bot.send_message(msg.chat.id, "ℹ️Вы уже являетесь пользователем этого бота.")
                goin(user_id, None, first_name)
            else:
                goin(user_id, referrer_candidate, first_name)
    else:
        goin(user_id, None, first_name)

    markupbut = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    startuchast = types.KeyboardButton('Принять участвие $')
    tablelid = types.KeyboardButton('Таблица лидеров🔝')
    infobot = types.KeyboardButton('Правила❕')
    markupbut.add(startuchast, tablelid, infobot)
    bot.send_message(msg.chat.id, "Главное меню",
                     reply_markup=markupbut)


@bot.message_handler(content_types=['text'])
def butanswer(message):
    if message.chat.type == 'private':
        if message.text == 'Принять участвие $':
            bot.send_message(message.chat.id,
                             "Приглашай друзей через свою реферальную ссылку и прими участие в реферальном "
                             "соревновании. "
                             "\n\n🎖50 призовых мест! "
                             "\n🥇1 место - 250 USDT!"
                             "\n🥈2 место - 150 USDT!"
                             "\n🏅3-5 места - 50 USDT!"
                             "\n🏅6-50 места - 10 USDT!\n\n"
                             "Для победы нужно всего лишь приглашать друзей по своей реферальной ссылка.\n\n"
                             "Ваша реферальная ссылка: "
                             "https://t.me/Airdrop_referal_bot?start=" + str(message.chat.id) + "\n\nВы "
                                                                                           "пригласили: " + str(
                                 numrefjust(message.chat.id)) + "👤\n\nСоревнования закончатся 15 июня.")

        elif message.text == 'Таблица лидеров🔝':
            bot.send_message(message.chat.id, top.top)

        elif message.text == 'Правила❕':
            bot.send_message(message.chat.id, "⚠️Вы можете приглашать рефералов только из стран СНГ. Платный трафик и "
                                              "накрутки запрещены. \n\nВ случае нарушения правил - ваш аккаунт будет "
                                              "заблокирован!")
        else:
            bot.reply_to(message, "Неизвестная команда!")
            bot.send_message(-611115582,message.from_user.first_name + ":  " + message.text)


def goin(user_id, reffer, first_name):
    """

    :type first_name: object
    """
    try:
        conn = sqlite3.connect("IdUser.bd")
        cursor = conn.cursor()
        newbot = cursor.execute("SELECT `id` FROM `Users` WHERE `user_id` = ?", (user_id,))
        if not bool(len(newbot.fetchall())):
            bot.send_message(699738143, "Новый пользователь.")
        result = cursor.execute("SELECT `id` FROM `Users` WHERE `user_id` = ?", (reffer,))
        if bool(len(result.fetchall())):
            bot.send_message(reffer, "Поздравляем! У вас новый реферал.")
            cursor.execute("UPDATE `Users` SET `nums_ref`=`nums_ref`+1 WHERE `user_id` = ?", (reffer,))
            cursor.execute("INSERT OR IGNORE INTO 'Users' ('user_id', 'referrer_id', 'first_name') VALUES(?,?,?)",
                           (user_id, reffer, first_name))
        cursor.execute("INSERT OR IGNORE INTO 'Users' ('user_id', 'referrer_id', 'first_name') VALUES(?,?,?)",
                       (user_id, None, first_name))

        conn.commit()

    except sqlite3.Error as error:
        print("Error", error)

    finally:
        if conn:
            conn.close()


def numrefjust(user_id):
    try:
        conn = sqlite3.connect("IdUser.bd")
        cursor = conn.cursor()
        nums = cursor.execute("SELECT `nums_ref` FROM `Users` WHERE `user_id` = ?", (user_id,))
        returnnums = nums.fetchall()[0][0]

    except sqlite3.Error as error:
        print("Error", error)

    finally:
        if conn:
            conn.close()
        try:
            return returnnums
        except:
            pass

def boolbot(user_id):
    try:
        conn = sqlite3.connect("IdUser.bd")
        cursor = conn.cursor()
        result = cursor.execute("SELECT `id` FROM `Users` WHERE `user_id` = ?", (user_id,))
        returbool = bool(len(result.fetchall()))

    except sqlite3.Error as error:
        print("Error", error)

    finally:
        if conn:
            conn.close()
        try:
            return returbool
        except:
            pass

bot.infinity_polling()
