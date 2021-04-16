from enum import Enum
import json
import os
from http.client import HTTPResponse
from requests import Response
import sqlite3
import time

from support.data_classes import DataType


class SQLiteCache:
    DB_NAME = 'cache.sqlite3'

    class DBTable(Enum):
        JSON_CACHE = "json_cache"
        CSV_CACHE = "csv_cache"

    class ResponseTypeError(Exception):
        def __init__(self, response):
            res_type = type(response)
            print(f"Error: unexpected response type. Type is: {res_type}")

    class DataTypeError(Exception):
        def __init__(self, data_type):
            data_type = type(data_type)
            print(f"Error: unexpected data type. Type is: {data_type}")

    def get_response_info(self, res):
        if isinstance(res, Response):
            table = self.DBTable.JSON_CACHE.value
            data = json.dumps(res.json())

        elif isinstance(res, HTTPResponse):
            table = self.DBTable.CSV_CACHE.value
            data = res.read()

        else:
            raise self.ResponseTypeError(res)

        return {"table": table, "data": data}

    def get_table(self, data_type):
        if data_type is DataType.JSON:
            return self.DBTable.JSON_CACHE.value
        if data_type is DataType.CSV:
            return self.DBTable.CSV_CACHE.value

    def __init__(self):
        """Create new database and db tables if not done yet. Initialize
        connection and cursor objects.
        """
        db_created = os.path.isfile(self.DB_NAME)
        self.con = sqlite3.connect(self.DB_NAME)
        self.cur = self.con.cursor()

        if not db_created:
            self.cur.execute("""CREATE TABLE json_cache
                                (url text, time float, data json)""")
            self.cur.execute("""CREATE TABLE csv_cache
                                            (url text, time float, data text)""")
            self.con.commit()

    def create_entry(self, res):
        """Store response object in SQL cache.

        Args:
            res (Union[requests.models.Response, http.client.HTTPResponse]):
                HTTP response from api call

        Returns:
            None
        """
        time_val = time.time()
        try:
            res_info = self.get_response_info(res)
            table = res_info['table']
            data_val = res_info['data']

        except self.ResponseTypeError:
            print("Unexpected response type.")
            return

        print(res_info)

        self.cur.execute(f"INSERT INTO {table} values(?, ?, ?)",
                         (res.url, time_val, data_val))
        self.con.commit()

    def read_entry(self, url, data_type):
        """Get response data (JSON) from SQL cache.

        Args:
            url (str): Alpha Vantage API url containing query params
            data_type (DataType): DataType enumeration, either CSV or JSON

        Returns:
            dict: JSON response from Alpha Vantage API
        """
        try:
            table = self.get_table(data_type)
        except self.DataTypeError as e:
            print(e)
            return

        self.cur.execute(f"SELECT data FROM {table} WHERE url = ?", (url,))
        data = self.cur.fetchone()

        return data

    def update_entry(self, res):
        """Update response object in SQL cache.

        Args:
            res (Union[requests.models.Response, http.client.HTTPResponse]):
                HTTP response from api call

        Returns:
            None
        """
        time_val = time.time()
        try:
            res_info = self.get_response_info(res)
            table = res_info['table']
            data_val = res_info['data']
        except self.ResponseTypeError as e:
            print(e)
            return

        self.cur.execute(f"UPDATE {table} SET time = ?, data = ? WHERE url = ?",
                         (time_val, data_val, res.url))
        self.con.commit()

    def is_recent(self, url, data_type, delta=60 * 5):
        """Check if HTTP response was stored a certain amount of time ago.
        Delta is in seconds and defaults to a length of 5 minutes.

        Args:
            url (str): Alpha Vantage API url containing query params
            data_type (DataType): DataType enumeration, either CSV or JSON
            delta (int): time delta in seconds

        Returns:
            bool: True if response was stored less than `delta` seconds ago,
                False otherwise
        """
        try:
            table = self.get_table(data_type)
        except self.DataTypeError:
            print("Unexpected data type.")
            return

        self.cur.execute(f'SELECT time FROM {table} WHERE url = ?', (url,))
        then = self.cur.fetchone()[0]
        now = time.time()

        return (now - then) <= delta
