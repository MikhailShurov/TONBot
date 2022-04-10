import telebot
from time import sleep


class bot:
    def __init__(self):
        self.bot = telebot.TeleBot('5049347663:AAHrg7oBpxXO_w5oeWaptAINCbkCKNojdYo')
        self.chat_id = 1140886668

    def send_require(self):
        self.bot.send_message(self.chat_id, "Подтверди вход по-братски")

    def send_crash_message(self):
        self.bot.send_message(self.chat_id, "Бот крашнулся, перезапусти его")
        self.bot.send_message(self.chat_id, "Файл с ошибкой:")
        with open("error.html", 'rb') as file:
            self.bot.send_document(self.chat_id, file)

    def send_information_to_make_a_post(self, title, genres, description):
        self.bot.send_message(self.chat_id, "Данные для нового поста")
        formatted_genres = ""
        for i in range(len(genres)):
            word = genres[i]
            if i != 0:
                word = str(genres[i]).lower()
            formatted_genres += word
            formatted_genres += ', '
        genres = formatted_genres[:-2]
        data = f'{title}\nЖанр: {genres}\n\n{description}'
        self.bot.send_message(self.chat_id, data)
        with open("image_for_post.jpg", 'rb') as file:
            self.bot.send_document(self.chat_id, file)
