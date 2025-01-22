import os
from dotenv import load_dotenv
from db import SakilaService
from ui import UserInterface
import constants as cn

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

user_interface = UserInterface()

sakila_service = None
try:
    sakila_service = SakilaService(config)
    sakila_service.connect()
except Exception as ex:
    user_interface.print_error(str(ex))
    exit(-1)

while True:
    user_interface.print_menu()
    user_input = user_interface.get_user_input().strip()
    if user_input == cn.GET_BY_TITLE_OPTION:
        title = user_interface.get_user_input("Input title: ")
        try:
            films = sakila_service.get_films_by_title(title.lower())
            user_interface.print_films(films)
        except Exception as ex:
            user_interface.print_error(str(ex))
    elif user_input == cn.GET_BY_GENRE_OPTION:
        try:
            genres = sakila_service.get_genres()
            user_interface.print_genres(genres)
        except Exception as ex:
            user_interface.print_error(str(ex))
            continue
        genre_id = user_interface.get_user_input("Input genre id: ")
        try:
            genre_name = None
            for genre in genres:
                if genre["category_id"] == int(genre_id):
                    genre_name = genre["name"]
                    break
            if not genre_name:
                user_interface.print_error("This genre number is not exist!")
                continue
            films = sakila_service.get_films_by_genre(int(genre_id), genre_name)
            user_interface.print_films(films)
        except Exception as ex:
            user_interface.print_error(str(ex))
    elif user_input == cn.GET_BY_YEAR_OPTION:
        year = user_interface.get_user_input("Input year: ")
        try:
            films = sakila_service.get_films_by_year(int(year))
            user_interface.print_films(films)
        except Exception as ex:
            user_interface.print_error(str(ex))
    elif user_input == cn.GET_TOP_10_SEARCH_QUERIES:
        try:
            search_queries = sakila_service.get_top_10_search_queries()
            user_interface.print_search_queries(search_queries)
        except Exception as ex:
            user_interface.print_error(str(ex))
    elif user_input == cn.EXIT_OPTION:
        break
    else:
        user_interface.print_error("Wrong input!")

sakila_service.close()