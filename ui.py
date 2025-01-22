import constants as cn


MENU_ITEMS = [
    (cn.GET_BY_TITLE_OPTION, "Get films by title"),
    (cn.GET_BY_GENRE_OPTION, "Get films by genre"),
    (cn.GET_BY_YEAR_OPTION, "Get films by year"),
    (cn.GET_TOP_10_SEARCH_QUERIES, "Get top 10 search queries"),
    (cn.EXIT_OPTION, "Exit"),
]


class UserInterface:
    def __init__(self): ...
    def print_menu(self) -> None:
        print("MENU")
        for option, msg in MENU_ITEMS:
            print(f"[{option}] {msg}")
    def get_user_input(self, prompt: str = ">> ") -> str:
        return input(prompt)
    def print_films(self, films: list) -> None:
        film_count = len(films)
        if film_count == 0:
            print("Films not found!")
            return
        pages = film_count // cn.FILM_COUNT_PER_PAGE
        if film_count % cn.FILM_COUNT_PER_PAGE != 0:
            pages += 1
        for p in range(pages):
            for film in films[p * cn.FILM_COUNT_PER_PAGE:(p + 1) * cn.FILM_COUNT_PER_PAGE]:
                self.__print_film(film)
            if p == pages - 1:
                break
            option = self.get_user_input("Do you want to see next page? [Yes]: ").strip().lower()
            if option not in ("", "y", "yes"):
                break
    def __print_film(self, film: dict) -> None:
        print(film["title"])
    def print_genres(self, genres: list) -> None:
        for g in genres:
            print(f"[{g["category_id"]}] {g["name"]}")
    def print_search_queries(self, search_queries: list) -> None:
        for query in search_queries:
            line = "Query by "
            if query["query_type"] == cn.QUERY_TYPE_TITLE:
                line += f"title with key '{query["key"]}' - {query["amount"]} times"
            elif query["query_type"] == cn.QUERY_TYPE_GENRE:
                line += f"genre with name '{query["key"].title()}' - {query["amount"]} times"
            elif query["query_type"] == cn.QUERY_TYPE_YEAR:
                line += f"year where year is {query["key"]} - {query["amount"]} times"
            print(line)
    def print_message(self, msg: str) -> None:
        print(msg)
    def print_error(self, msg: str) -> None:
        print(f"Error: {msg}")