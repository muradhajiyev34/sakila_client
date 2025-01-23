#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from dotenv import load_dotenv
from db import SakilaService  # Import the database service class
from ui import UserInterface  # Import the user interface class
import constants as cn

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def main() -> int:
    """
    Main function for the film searching application.

    Handles the main program loop, user interactions, and database operations.

    Returns:
    - int: Exit code (0 for success, -1 for failure).
    """
    user_interface = UserInterface()  # Create a UserInterface object

    sakila_service = None
    try:
        sakila_service = SakilaService(config)  # Create a database service object
        sakila_service.connect()  # Establish a connection to the database
    except Exception as ex:
        user_interface.print_error("Connection failure!")
        return -1

    while True:
        user_interface.print_menu()  # Display the main menu
        user_input = user_interface.get_user_input().strip()

        if user_input == cn.GET_BY_TITLE_OPTION:
            # Get films by title option
            title = user_interface.get_user_input("Input title: ")
            if "'" in title:
                user_interface.print_error("Title can't contain \"'\" symbol!")
                continue
            try:
                films = sakila_service.get_films_by_title(title.lower())
                user_interface.print_films(films)
            except Exception as ex:
                user_interface.print_error(str(ex))

        elif user_input == cn.GET_BY_GENRE_OPTION:
            # Get films by genre option
            try:
                genres = sakila_service.get_genres()
                user_interface.print_genres(genres)
            except Exception as ex:
                user_interface.print_error(str(ex))
                continue
            try:
                genre_id = int(user_interface.get_user_input("Input genre id: "))
                genre_name = None
                for genre in genres:
                    if genre["category_id"] == genre_id:
                        genre_name = genre["name"]
                        break
                if not genre_name:
                    user_interface.print_error("This genre number is not exist!")
                    continue
                films = sakila_service.get_films_by_genre(genre_id, genre_name)
                user_interface.print_films(films)
            except ValueError as ex:
                user_interface.print_error("Genre id is must be a number!")
            except Exception as ex:
                user_interface.print_error(str(ex))

        elif user_input == cn.GET_BY_YEAR_OPTION:
            # Get films by year option
            try:
                year = int(user_interface.get_user_input("Input year: "))
                films = sakila_service.get_films_by_year(year)
                user_interface.print_films(films)
            except ValueError as ex:
                user_interface.print_error("Year is must be a number!")
            except Exception as ex:
                user_interface.print_error(str(ex))

        elif user_input == cn.GET_TOP_10_SEARCH_QUERIES:
            # Get top 10 search queries option
            try:
                search_queries = sakila_service.get_top_10_search_queries()
                user_interface.print_search_queries(search_queries)
            except Exception as ex:
                user_interface.print_error(str(ex))

        elif user_input == cn.EXIT_OPTION:
            # Exit the program
            break

        else:
            user_interface.print_error("Wrong input!")

    sakila_service.close()  # Close the database connection
    return 0


if __name__ == "__main__":
    exit(main())

