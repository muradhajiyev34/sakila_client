import constants as cn

# Menu items with corresponding options and descriptions
MENU_ITEMS = [
    (cn.GET_BY_TITLE_OPTION, "Get films by title"),
    (cn.GET_BY_GENRE_OPTION, "Get films by genre"),
    (cn.GET_BY_YEAR_OPTION, "Get films by year"),
    (cn.GET_TOP_10_SEARCH_QUERIES, "Get top 10 search queries"),
    (cn.EXIT_OPTION, "Exit"),
]

class UserInterface:
    """
    A class to handle the user interface for a film management application.
    Provides methods for displaying menus, films, genres, and search queries,
    as well as handling user input.
    """

    def __init__(self):
        """Initializes the UserInterface class."""
        ...

    def print_menu(self) -> None:
        """
        Prints the main menu with available options.
        """
        print("MENU")
        for option, msg in MENU_ITEMS:
            print(f"[{option}] {msg}")

    def get_user_input(self, prompt: str = ">> ") -> str:
        """
        Gets input from the user.

        Parameters:
        - prompt (str): The input prompt to display to the user.

        Returns:
        - str: The user input as a string.
        """
        return input(prompt)

    def print_films(self, films: list) -> None:
        """
        Prints a paginated list of films.

        Parameters:
        - films (list): A list of dictionaries, where each dictionary contains film details.
        """
        film_count = len(films)
        if film_count == 0:
            print("Films not found!")
            return

        # Calculate the number of pages required for pagination
        pages = film_count // cn.FILM_COUNT_PER_PAGE
        if film_count % cn.FILM_COUNT_PER_PAGE != 0:
            pages += 1

        # Print films page by page
        for p in range(pages):
            for film in films[p * cn.FILM_COUNT_PER_PAGE:(p + 1) * cn.FILM_COUNT_PER_PAGE]:
                self.__print_film(film)
            if p == pages - 1:
                break  # Stop after the last page

            # Ask the user if they want to proceed to the next page
            option = self.get_user_input("Do you want to see next page? [Yes]: ").strip().lower()
            if option not in ("", "y", "yes"):
                break

    def __print_film(self, film: dict) -> None:
        """
        Prints the details of a single film.

        Parameters:
        - film (dict): A dictionary containing film details (e.g., title).
        """
        print(film["title"])

    def print_genres(self, genres: list) -> None:
        """
        Prints a list of genres with their IDs.

        Parameters:
        - genres (list): A list of dictionaries, where each dictionary contains genre details.
        """
        for g in genres:
            print(f"[{g['category_id']}] {g['name']}")

    def print_search_queries(self, search_queries: list) -> None:
        """
        Prints a list of search queries along with their statistics.

        Parameters:
        - search_queries (list): A list of dictionaries, where each dictionary contains
          query details such as type, key, and amount.
        """
        for query in search_queries:
            line = "Query by "
            if query["query_type"] == cn.QUERY_TYPE_TITLE:
                line += f"title with key '{query['key']}' - {query['amount']} times"
            elif query["query_type"] == cn.QUERY_TYPE_GENRE:
                line += f"genre with name '{query['key'].title()}' - {query['amount']} times"
            elif query["query_type"] == cn.QUERY_TYPE_YEAR:
                line += f"year where year is {query['key']} - {query['amount']} times"
            print(line)

    def print_message(self, msg: str) -> None:
        """
        Prints a general message.

        Parameters:
        - msg (str): The message to print.
        """
        print(msg)

    def print_error(self, msg: str) -> None:
        """
        Prints an error message.

        Parameters:
        - msg (str): The error message to print.
        """
        print(f"Error: {msg}")
