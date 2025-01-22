import pymysql.cursors
from exceptions import DataBaseConnectionError
import constants as cn


class SakilaService:
    def __init__(self, connection_config: dict):
        self.__config = connection_config
        self.__connection = None
    
    def connect(self) -> None:
        if not self.__connection:
            self.__connection = pymysql.connect(
                **self.__config,
                cursorclass=pymysql.cursors.DictCursor
            )
            
    def close(self) -> None:
        if self.__connection:
            self.__connection.close()
        self.__connection = None

    def get_films_by_title(self, title: str) -> list:
        query = f"SELECT * FROM film f WHERE f.title LIKE '%{title}%';"
        result = self.__execute_query(query)
        self.__write_to_archive(title, cn.QUERY_TYPE_TITLE)
        return result
        
    def get_films_by_genre(self, genre_id: int, genre_name: str) -> list:
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
        self.__write_to_archive(genre_name, cn.QUERY_TYPE_GENRE)
        return result
        
    def get_films_by_year(self, year: int) -> list:
        """
        Returns ....
        """
        query = f"SELECT * FROM film f WHERE f.release_year = {year};"
        result = self.__execute_query(query)
        self.__write_to_archive(str(year), cn.QUERY_TYPE_YEAR)
        return result

    def get_genres(self) -> list:
        query = f"SELECT * FROM category c ORDER BY c.category_id;"
        return self.__execute_query(query)

    def get_top_10_search_queries(self):
        query = f"SELECT * FROM search_archive sa ORDER BY sa.amount DESC LIMIT 10;"
        return self.__execute_query(query)
    
    def __write_to_archive(self, key: str, query_type: int) -> None:
        query1 = f"""UPDATE search_archive sa
            SET sa.amount = sa.amount + 1
            WHERE sa.key = '{key}' AND sa.query_type = {query_type};"""
        query2 = f"INSERT INTO search_archive(`key`, query_type) VALUES ('{key}', {query_type});"
        if not self.__connection:
            raise DataBaseConnectionError()
        with self.__connection.cursor() as cursor:    
            cursor.execute(query1)
            self.__connection.commit()
            if cursor.rowcount == 0:
                cursor.execute(query2)
                self.__connection.commit()

    def __execute_query(self, query: str) -> list:
        if not self.__connection:
            raise DataBaseConnectionError()
        with self.__connection.cursor() as cursor:    
            cursor.execute(query)
            return cursor.fetchall()