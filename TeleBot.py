import telebot


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
        formatted_genres = str(genres[0] + ', ') + ''.join(str(genres[i].lower() + ', ') for i in range(len(genres)) if i != 0)
        genres = formatted_genres[:-2]
        data = f'Название: {title}\n\nЖанры: {genres}\n\nОписание: {description}'
        self.bot.send_message(self.chat_id, data)
        with open("image_for_post.jpg", 'rb') as file:
            self.bot.send_document(self.chat_id, file)
