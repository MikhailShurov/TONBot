import requests
import json
from random import seed, randint
from time import sleep


class worker:
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

    def ton_auth(self):
        print('auth')

    def parse_info(self):
        seed(randint(0, 100))
        selected_genre = self.movie_genres[randint(0, len(self.movie_genres) - 1)]

        response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key={self.api_key}&with_genres={selected_genre}&language={self.language}&page={randint(0, 101)}')
        response = json.loads(response.text)

        selected_film = randint(0, 21)
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

        print(self.title)
        print(self.genres)
        print(self.description)

    def make_a_post(self):
        print('posted')


if __name__ == '__main__':
    w = worker()
    try:
        w.ton_auth()
        while True:
            w.parse_info()
            w.make_a_post()
            sleep(28800)  # 8 hours
    except Exception as ex:
        print(ex)
