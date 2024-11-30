# from config import Config, load_config
import telebot

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

# Создаем объекты бота и диспетчера
# bot = Bot(BOT_TOKEN)

bot = telebot.TeleBot('8029690887:AAHP9TURI66OsdCdXeCQSlPiz0GF1UWC3hw')

@bot.message_handler(commands=['start'])
def send_welcome(message):
        bot.send_message(message.chat.id, "Привет! здесь можно рассчитать темп, время или расстояние.")
        bot.send_message(message.chat.id, "выберите одну из команд: /pace, /time, /distance")
 
@bot.message_handler(commands=['pace'])

def enter_time(message):
    time = bot.send_message(message.chat.id, 'введите время в секундах') 
    bot.register_next_step_handler(time, enter_distance)

def enter_distance(message):
    global time;
    time = message.text
    distance = bot.send_message(message.chat.id, 'введите расстояние в метрах') 
    bot.register_next_step_handler(distance, result)
    
def result(message):
    global distance;
    distance = message.text
    pace = (int(time)/60)/(int(distance)/1000)
    p_min= int(pace//1)
    p_sec = int(pace%1*60)
    bot.send_message(message.chat.id, (f'Ваш темп составил {p_min} мин {p_sec} сек'))

 
@bot.message_handler(commands=['time'])

def enter_pace_time(message):
    global pace;
    pace = bot.send_message(message.chat.id, 'введите темп в секундах') 
    bot.register_next_step_handler(pace, enter_distance_time)

def enter_distance_time(message):
    global pace;
    global distance;
    pace = message.text
    distance = bot.send_message(message.chat.id, 'введите расстояние в метрах') 
    bot.register_next_step_handler(distance, result_time)
    
def result_time(message):
    global time;
    global distance;
    distance = message.text
    time  = int(pace) * int(distance) /60/1000
    t_min= int(time//1)
    t_sec = int(time%1*60)
    bot.send_message(message.chat.id, (f'Ваше время составило {t_min} мин {t_sec} сек'))
    
@bot.message_handler(commands=['distance'])

def enter_time_distance(message):
    global time;
    time = bot.send_message(message.chat.id, 'введите время в секундах') 
    bot.register_next_step_handler(time, enter_pace_distance)

def enter_pace_distance(message):
    global pace;
    global time;
    time = message.text
    pace = bot.send_message(message.chat.id, 'введите темп в секундах') 
    bot.register_next_step_handler(pace, result_distance)
    
def result_distance(message):
    global pace;
    global distance;
    pace = message.text
    distance = int(time)/int(pace)
    bot.send_message(message.chat.id, (f'Ваше расстояние составило {round(distance,1)} км или {int(distance*1000//1)} м'))
    
    
bot.polling(none_stop=True) 