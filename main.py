import telebot
from telebot import types
from data import db_session
from data.users import User
from sqlalchemy import func, or_
from data.markups import markups

bot = telebot.TeleBot("6122208462:AAGVF5U1DQDc3bXPETrF5fawQBLsVKvum7M", parse_mode=None)
db_session.global_init("data/db.db")
markup_standart = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("/start")
markup_standart.add(btn1)
room = 1
db_sess = db_session.create_session()
for baseUser in db_sess.query(User):
    bot.send_message(baseUser.tid, "Привет, бот был перезапущен, нужно заново пройти регистрацию(/start),"
                                   " извини за неудобство")
    db_sess.query(User).filter(User.tid == baseUser.tid).first().doing = "nothing"
    db_sess.query(User).filter(User.tid == baseUser.tid).first().room = 0
db_sess.commit()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я - анонимный бот, с помощью меня ты можешь общаться со случайным "
                                      "человеком инкогнито!"
                                      " Для регистрации нужно всего лишь указать свой пол :)",
                     reply_markup=markups["sex"])
    bot.register_next_step_handler(message, registration)


def registration(message):
    user = User()
    user.tid = message.from_user.id
    if message.text == "♂Мужской♂":
        user.sex = 1
    elif message.text == "♀Женский♀":
        user.sex = 0
    else:
        bot.send_message(message.from_user.id, "Нужно выбрать пол")
        bot.register_next_step_handler(message, registration)
        return
    user.doing = 'nothing'
    user.room = 0
    user.searching_for = -1
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.tid == message.from_user.id).first():
        db_sess.add(user)
        db_sess.commit()
    elif db_sess.query(User).filter(User.tid == message.from_user.id).first().sex == user.sex:
        bot.send_message(message.from_user.id, 'Вы уже зарегистрированы!')
    else:
        db_sess.query(User).filter(User.tid == message.from_user.id).first().sex = user.sex
        bot.send_message(message.from_user.id, 'Разраб верит в смену пола')
        db_sess.commit()
    bot.send_message(message.from_user.id, 'Итак, кого бы вы хотели найти для общения?', reply_markup=markups["find"])
    bot.register_next_step_handler(message, startsearching)


def startsearching(message):
    global room
    db_sess = db_session.create_session()
    if message.text in ['Девушку', 'Парня', 'Не важно']:
        if db_sess.query(User.doing).filter(User.tid == message.from_user.id).scalar() == 'nothing':
            sex_id = ['Девушку', 'Парня', 'Не важно'].index(message.text)
            user = db_sess.query(User).filter(User.tid == message.from_user.id).first()
            user.searching_for = sex_id
            user.doing = 'searching'
            bot.send_message(message.from_user.id, 'Ищу🔎', reply_markup=markups["stopsearching"])
            bot.register_next_step_handler(message, conversation)
            if sex_id != 2:
                partner = db_sess.query(User).filter(User.doing == 'searching', or_(User.searching_for == 2,
                                                                                    User.searching_for == user.sex),
                                                     User.tid != message.from_user.id, User.sex == sex_id) \
                    .order_by(func.random()).first()
            else:
                partner = db_sess.query(User).filter(User.doing == 'searching', or_(User.searching_for == 2,
                                                                                    User.searching_for == user.sex),
                                                     User.tid != message.from_user.id) \
                    .order_by(func.random()).first()
            if partner:
                user.doing = 'chatting'
                partner.doing = 'chatting'
                user.room = room
                partner.room = room
                db_sess.commit()
                bot.send_message(message.from_user.id, 'Нашел тебе друга, можешь с ним переписываться!',
                                 reply_markup=markups["stoptalking"])
                bot.send_message(partner.tid, 'Нашел тебе друга, можешь с ним переписываться!',
                                 reply_markup=markups["stoptalking"])
                room += 1
    else:
        bot.send_message(message.from_user.id, 'Для поиска нужно указать желаемый пол', reply_markup=markups["find"])
        bot.register_next_step_handler(message, startsearching)
    db_sess.commit()


def conversation(message):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.tid == message.from_user.id).first()
    if user.doing == "chatting":
        global room
        partner = db_sess.query(User).filter(User.tid != message.from_user.id, User.room == user.room).first()
        if message != 'Закончить разговор':
            bot.send_message(partner.tid, message.text)
            print("Message was sent")
            bot.register_next_step_handler(message, conversation)
        else:
            user.room = 0
            user.doing = "nothing"
            partner.room = 0
            partner.doing = "nothing"
            bot.register_next_step_handler(message, conversation)
    elif user.doing == "nothing":
        bot.send_message(user.tid, "Кажется, разговор был завершён, ищем дальше...?", reply_markup=markups["find"])
        bot.register_next_step_handler(message, startsearching)
    elif user.doing == "searching" and message.text == "Остановить поиск":
        user.doing = "nothing"
        bot.send_message(user.tid, "Поиск остановлен, кого будем искать?", reply_markup=markups["find"])
        bot.register_next_step_handler(message, startsearching)
    elif user.doing == "searching" and message.text != "Остановить поиск":
        bot.register_next_step_handler(message, conversation)
    db_sess.commit()


bot.infinity_polling()
