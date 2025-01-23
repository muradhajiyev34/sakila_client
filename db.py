import pymysql.cursors
from exceptions import DataBaseConnectionError
import constants as cn


class SakilaService:
    """
    A service class to interact with the Sakila database.
    Provides methods to retrieve films, genres, and search queries, as well as
    to log search activity into an archive.
    """

    def __init__(self, connection_config: dict):
        """
        Initializes the SakilaService with a database connection configuration.

        Parameters:
        - connection_config (dict): Configuration for connecting to the database.
        """
        self.__config = connection_config
        self.__connection = None

    def connect(self) -> None:
        """
        Establishes a connection to the database using the provided configuration.
        """
        if not self.__connection:
            self.__connection = pymysql.connect(
                **self.__config,
                cursorclass=pymysql.cursors.DictCursor
            )

    def close(self) -> None:
        """
        Closes the database connection if it is open.
        """
        if self.__connection:
            self.__connection.close()
        self.__connection = None

    def get_films_by_title(self, title: str) -> list:
        """
        Retrieves films whose titles contain the specified substring.

        Parameters:
        - title (str): The substring to search for in film titles.

        Returns:
        - list: A list of films that match the search criteria.
        """
        query = f"SELECT * FROM film f WHERE f.title LIKE '%{title}%';"
        result = self.__execute_query(query)
        self.__write_to_archive(title, cn.QUERY_TYPE_TITLE)  # Log the query
        return result

    def get_films_by_genre(self, genre_id: int, genre_name: str) -> list:
        """
        Retrieves films that belong to a specific genre.

        Parameters:
        - genre_id (int): The ID of the genre.
        - genre_name (str): The name of the genre.

        Returns:
        - list: A list of films in the specified genre.
        """
        query = f"""
            SELECT f.title, c.name AS category_name
            FROM 
                film AS f
                    JOIN
                film_category AS fc ON f.film_id = fc.film_id
                    JOIN 
                category AS c ON fc.category_id = c.category_id
            WHERE c.category_id = {genre_id};"""
        result = self.__execute_query(query)
        self.__write_to_archive(genre_name, cn.QUERY_TYPE_GENRE)  # Log the query
        return result

    def get_films_by_year(self, year: int) -> list:
        """
        Retrieves films that were released in a specific year.

        Parameters:
        - year (int): The release year to filter films.

        Returns:
        - list: A list of films released in the specified year.
        """
        query = f"SELECT * FROM film f WHERE f.release_year = {year};"
        result = self.__execute_query(query)
        self.__write_to_archive(str(year), cn.QUERY_TYPE_YEAR)  # Log the query
        return result

    def get_genres(self) -> list:
        """
        Retrieves all genres from the database.

        Returns:
        - list: A list of genres, each represented as a dictionary.
        """
        query = f"SELECT * FROM category c ORDER BY c.category_id;"
        return self.__execute_query(query)

    def get_top_10_search_queries(self) -> list:
        """
        Retrieves the top 10 most frequent search queries from the archive.

        Returns:
        - list: A list of the top 10 search queries.
        """
        query = f"SELECT * FROM search_archive sa ORDER BY sa.amount DESC LIMIT 10;"
        return self.__execute_query(query)

    def __write_to_archive(self, key: str, query_type: int) -> None:
        """
        Logs the search query into the search_archive table.
        If the query already exists, its count is incremented. Otherwise, a new entry is created.

        Parameters:
        - key (str): The search key (e.g., title, genre name, or year).
        - query_type (int): The type of query.

        Raises:
        - DataBaseConnectionError: If the database connection is not established.
        """
        query1 = f"""UPDATE search_archive sa
            SET sa.amount = sa.amount + 1
            WHERE sa.key = '{key}' AND sa.query_type = {query_type};"""
        query2 = f"INSERT INTO search_archive(`key`, query_type) VALUES ('{key}', {query_type});"
        if not self.__connection:
            raise DataBaseConnectionError()  # Ensure a connection exists
        with self.__connection.cursor() as cursor:
            cursor.execute(query1)
            self.__connection.commit()
            if cursor.rowcount == 0:  # If no rows were updated, insert a new entry
                cursor.execute(query2)
                self.__connection.commit()

    def __execute_query(self, query: str) -> list:
        """
        Executes a SQL query and returns the results.

        Parameters:
        - query (str): The SQL query to execute.

        Returns:
        - list: A list of results, each represented as a dictionary.

        Raises:
        - DataBaseConnectionError: If the database connection is not established.
        """
        if not self.__connection:
            raise DataBaseConnectionError()  # Ensure a connection exists
        with self.__connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
