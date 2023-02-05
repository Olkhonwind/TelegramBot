import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'Привет', 'привет'])
def start(message: telebot.types.Message):
    text = 'Привет! \nЯ чат-бот "IrkBot" и помогу Вам конвертировать валюту. \
Чтобы увидеть все доступные валюты нажмите или наберите: /values \
Чтобы начать работу введите команду в следующем формате: \n<имя валюты, цену которой Вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \<количество первой валюты>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Необходимо ввести команду в следующем формате: \n<имя валюты, цену которой Вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nНапример: евро доллар 1'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список доступных валют: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('В команде присутствуют лишние параметры (символы)')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}. Повторите команду или нажмите сюда: /help')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}. Повторите команду или нажмите сюда: /help')
    else:
        text = f'Стоимость {amount} {quote} в {base} составляет: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
