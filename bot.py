import json
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup

token = ""
bot=TeleBot(token=token)

def read_json(file_name="players.json"):
    with open(file_name, "r", encoding="utf-8-sig") as file:
        return json.load(file)

def write_json(data, file_name="players.json"):
    with open(file_name, "w") as file:
        json.dump(data, file)


locations = read_json("location.json")
players = read_json()

def new_player(player_id):
    if player_id not in players:
        players[player_id] = {"location": "home"}
        write_json(players)
        send_info(player_id)
        return True
    return False

def send_info(player_id):
    print(players, locations)
    text = locations[players[player_id]['location']]['description']
    img = str(locations[players[player_id]['location']]['image'])
    print(img)
    actions = list(locations[players[player_id]['location']]['actions'].keys())
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*actions)
    bot.send_photo(player_id, photo=img, caption=text, reply_markup=menu_keyboard)

@bot.message_handler(commands=["start"])
def Start(message):
    menu_keyboard =ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*['/перемога', '/играть'])
    bot.send_message(message.from_user.id, "думай сам как начать играть", reply_markup=menu_keyboard)

@bot.message_handler(commands=['перемога', 'help'])
def Help(message):
    bot.send_message(message.from_user.id, "/help, /перемога - помощь\n/start - у тут понятно это запуск бота\n/play,/играть - начать незабываемое приключение после которого ты окажешься психически неуравновешеным")
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*['/играть'])

@bot.message_handler(commands=['играть', 'play'])
def play(message):
    player_id = str(message.from_user.id)
    if new_player(player_id): return
    send_info(player_id)

@bot.message_handler(func=lambda message: True)
def engine(message):
    player_id = str(message.from_user.id)
    if new_player(player_id): return
    try:
        p_new_location = locations[players[player_id]['location']]['actions'][message.text]
        players[player_id]['location'] = p_new_location
        exec(locations[players[player_id]['location']].get("def", ""))
        write_json(players)
        send_info(player_id)
    except:
        bot.send_message((player_id, "неправильно"))
bot.infinity_polling()