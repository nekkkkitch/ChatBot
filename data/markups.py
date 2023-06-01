import telebot
from telebot import types


markup_find = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnfindman = types.KeyboardButton("Парня")
btnfindwoman = types.KeyboardButton("Девушку")
btnfindanyone = types.KeyboardButton("Не важно")
markup_find.add(btnfindman, btnfindwoman, btnfindanyone)
markup_sex = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnsexm = types.KeyboardButton("♂Мужской♂")
btnsexw = types.KeyboardButton("♀Женский♀")
markup_sex.add(btnsexm, btnsexw)
markup_stopsearching = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnstopsearching = 'Остановить поиск'
markup_stopsearching.add(btnstopsearching)
markup_stoptalking = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnstoptalking = 'Закончить разговор'
markup_stoptalking.add(btnstoptalking)
markups = {"sex": markup_sex, "find": markup_find, "stopsearching": markup_stopsearching, "stoptalking": markup_stoptalking}
