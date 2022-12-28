import telebot
from telebot import types
import random
import psycopg2
from mytokenexport import token, password

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    user="postgres",
    password=password)

    cur = conn.cursor()

    cur.execute(f"SELECT username FROM myusers WHERE username = '{message.from_user.username}'")
    data = cur.fetchone()
    print(data)

    if data is None:
        cur.execute('INSERT INTO myusers (username) VALUES (%s)', (message.from_user.username,))
        conn.commit()
        cur.close()
        conn.close()
        print(message.from_user.username)
    bot.send_message(message.chat.id, 'Привет игра "<b>Камень ножницы бумага</b>"\n Напиши /start1 для начала игры', parse_mode='html')

games_score = {}

def set_score(user_id, score):
  if not user_id in games_score:
    games_score[user_id] = score
  else:
    games_score[user_id] += score
  return games_score[user_id]

@bot.message_handler(content_types=['text'])
def game(message):
    player = message.text
    bot1 = random.randint(1,3)
    match player, bot1:
        case '/start1', _:
            games_score[message.from_user.id] = 0
            games_score[message.from_user.id*2] = 0
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            kam = types.KeyboardButton('Камень' )
            noj = types.KeyboardButton('Ножницы')
            bum = types.KeyboardButton('Бумага')
            markup.add(kam, noj, bum)
            bot.send_message(message.chat.id, f'<b>Начинай!\nПиши "/start1" для начала новой игры</b>' ,parse_mode='html', reply_markup = markup)
        case "Камень", 2:
            bot.send_message(message.chat.id , '<b>Ножницы!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Вы выиграли!')
            set_score(message.from_user.id, 1)
            set_score(message.from_user.id*2, 0)
            bot.send_message(message.chat.id, f'Счет: <b>{games_score[message.from_user.id]}:{games_score[message.from_user.id*2]}</b>', parse_mode='html')
        case "Бумага", 1:
            bot.send_message(message.chat.id , '<b>Камень!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Вы выиграли!')
            set_score(message.from_user.id, 1)
            set_score(message.from_user.id*2, 0)
            bot.send_message(message.chat.id, f'Счет: <b>{games_score[message.from_user.id]}:{games_score[message.from_user.id*2]}</b>', parse_mode='html')
        case "Ножницы", 3:
            bot.send_message(message.chat.id , '<b>Бумага!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Вы выиграли!')
            set_score(message.from_user.id, 1)
            set_score(message.from_user.id*2, 0)
            bot.send_message(message.chat.id, f'Счет: <b>{games_score[message.from_user.id]}:{games_score[message.from_user.id*2]}</b>', parse_mode='html')
        case 'Бумага', 2:    
            bot.send_message(message.chat.id , '<b>Ножницы!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Вы проиграли!')
            set_score(message.from_user.id*2, 1)
            set_score(message.from_user.id, 0)
            bot.send_message(message.chat.id, f'Счет: <b>{games_score[message.from_user.id]}:{games_score[message.from_user.id*2]}</b>', parse_mode='html')
        case "Камень", 3:
            bot.send_message(message.chat.id , '<b>Бумага!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Вы проиграли!')
            set_score(message.from_user.id*2, 1)
            set_score(message.from_user.id, 0)
            bot.send_message(message.chat.id, f'Счет: <b>{games_score[message.from_user.id]}:{games_score[message.from_user.id*2]}</b>', parse_mode='html' )
        case "Ножницы", 1:
            bot.send_message(message.chat.id , '<b>Камень!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Вы проиграли!')
            set_score(message.from_user.id*2, 1)
            set_score(message.from_user.id, 0)
            bot.send_message(message.chat.id, f'Счет: <b>{games_score[message.from_user.id]}:{games_score[message.from_user.id*2]}</b>', parse_mode='html' )
        case "Ножницы", 2:
            bot.send_message(message.chat.id , '<b>Ножницы!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Ничья!')
        case "Камень", 1:
            bot.send_message(message.chat.id , '<b>Камень!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Ничья!')
        case "Бумага", 3:
            bot.send_message(message.chat.id , '<b>Бумага!</b>', parse_mode='html')
            bot.send_message(message.chat.id , 'Ничья!')

        case "allpl", _:
            conn = psycopg2.connect(
            host="localhost",
            database="testdb",
            user="postgres",
            password="lol")
            cur = conn.cursor()

            cur.execute("SELECT username FROM myusers ORDER BY id")
            data = cur.fetchall()
            print(data)

            sc = 0
            
            print(data[0])

            l = len(data)
            for i in range(l):
                for j in data[sc]:
                    bot.send_message(message.chat.id, f'{j}')
                    print(j)
                    sc += 1
            print(l)
            bot.send_message(message.chat.id, f'{l}')
        case "school", _:
            conn = psycopg2.connect(
            host="localhost",
            database="testdb",
            user="postgres",
            password="lol")
            cur = conn.cursor()

            cur.execute("SELECT username FROM myusers WHERE from_where = 'School'")
            data = cur.fetchall()
            print(data)
            sc = 0
            print(data[0])
            l = len(data)
            print(l)
            for i in range(l):
                for j in data[sc]:
                    bot.send_message(message.chat.id, f'{j}')
                    print(j)
                    sc += 1
            bot.send_message(message.chat.id, f'{l}')                
            
bot.polling(none_stop=True)