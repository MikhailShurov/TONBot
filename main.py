import os

import requests
import json

from random import seed, randint
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import TeleBot

from rich.console import Console
from rich.traceback import install

install()
console = Console(record=True)


class Worker:
    def __init__(self):
        self.title = None
        self.genres = []
        self.description = None
        self.image = None
        self.genres_values = {28: "Боевик",
                              37: "Вестерн",
                              10752: "Военный",
                              9648: "Детектив",
                              99: "Документальный",
                              18: "Драма",
                              36: "История",
                              35: "Комедия",
                              80: "Криминал",
                              10749: "Мелодрама",
                              10402: "Музыка",
                              16: "Мультфильм",
                              12: "Приключения",
                              10751: "Семейный",
                              10770: "Телефильм",
                              53: "Триллер",
                              27: "Ужасы",
                              878: "Фантастика",
                              14: "Фэнтези"}

        self.movie_genres = [28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37]
        self.posted_ids = [0]

        self.api_key = '51201bea16768dcaccd8a5c90e6c7972'
        self.language = 'ru-RU'

        self.bot = TeleBot.bot()

        chrome_options = webdriver.ChromeOptions()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def ton_auth(self):
        self.browser.get('https://ton.place/')
        self.browser.save_screenshot("norm1.png")
        self.browser.find_element_by_class_name('Button__text').click()
        active_windows = self.browser.window_handles
        self.browser.switch_to.window(active_windows[1])
        sleep(3)
        self.browser.find_element_by_id('login-phone').send_keys('29671')
        self.browser.find_element_by_id('login-phone').send_keys('1001')
        sleep(3)
        self.browser.save_screenshot("norm2.png")
        buttons_group = self.browser.find_elements_by_class_name('button-item-label')
        buttons_group[1].click()
        sleep(10)
        self.browser.switch_to.window(active_windows[0])
        sleep(10)
        self.browser.save_screenshot("norm3.png")
        self.bot.send_require()

    def parse_info(self):
        seed(randint(0, 100))
        selected_genre = self.movie_genres[randint(0, len(self.movie_genres) - 1)]

        response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={self.api_key}&with_genres={selected_genre}&language={self.language}&page={randint(0, 101)}')
        response = json.loads(response.text)

        selected_film = randint(0, 19)
        if response["results"][selected_film]["id"] in self.posted_ids:
            self.parse_info()
            return

        self.title = response["results"][selected_film]["title"]
        self.genres = response["results"][selected_film]["genre_ids"]
        for i in range(len(self.genres)):
            self.genres[i] = self.genres_values[self.genres[i]]
        self.description = response["results"][selected_film]['overview']

        if self.title == "" or self.genres == [] or self.description == "":
            self.parse_info()
            return

        self.image = requests.get(f'https://image.tmdb.org/t/p/w500/{response["results"][selected_film]["poster_path"]}').content
        with open('image_for_post.jpg', 'wb') as file:
            file.write(self.image)

    def make_a_post(self):
        self.bot.send_information_to_make_a_post(self.title, self.genres, self.description)


if __name__ == '__main__':
    w = Worker()
    try:
        w.ton_auth()
        while True:
            w.parse_info()
            w.make_a_post()
            sleep(18000)  # 6 hours
    except:
        console.print_exception()
        console.save_html("error.html")
        sleep(3)
        w.bot.send_crash_message()
