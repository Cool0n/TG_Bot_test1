import telebot
import schedule
import requests
import time
import auth_data
from multiprocessing import Pool

token = auth_data.token
channel_id = auth_data.channel_id


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Welcome my friend!")
        print(f'message.chat.id = {message.chat.id}, channel_id = {channel_id}')

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "hello":
            bot.send_message(message.chat.id, "Hello dude!")
        else:
            bot.send_message(message.chat.id, "Something wrong!")

    bot.polling()


def some_text(token, channel_id):
    print(f"channel_id = {channel_id}")
    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": "Write something every 5 sec"
    })
    if r.status_code != 200:
        raise Exception("post_text error")


def repeat():
    # time.sleep(5)
    # schedule.every(5).seconds.do(some_text(token, channel_id))
    # while True:
    #     schedule.run_pending()

    while True:
        time.sleep(5)
        some_text(token, channel_id)


def main(start):
    if start == 1:
        telegram_bot(token)
    if start == 2:
        repeat()


if __name__ == '__main__':
    start = [1, 2]
    p = Pool(processes=2)
    p.map(main, start)
