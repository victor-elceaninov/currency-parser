from abc import abstractmethod
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup

import config


class ParseService:
    __url = config.URL
    __headers = config.HEADERS
    __exclusion = ()
    __data = []

    @abstractmethod
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise Exception(exc_val)

    def set_url(self, url):
        self.__url = url

    def get_data(self):
        return self.__data

    def set_exclusion(self, data):
        self.__exclusion = data

    def get_exclusion(self):
        return self.__exclusion

    def start(self):
        try:
            data_from_url = self.__get_data_from_url()
        except Exception as err:
            raise err
        else:
            soup = BeautifulSoup(data_from_url.content, config.PARSER)
            self.__data = self.extract_data(soup)
            return self.to_dictionary()

    def __get_data_from_url(self):
        try:
            response = requests.get(self.__url, headers=self.__headers)
            response.raise_for_status()
        except HTTPError as http_err:
            raise http_err
        except Exception as err:
            raise err
        else:
            return response

    @abstractmethod
    def extract_data(self, soup):
        pass

    @abstractmethod
    def to_dictionary(self):
        pass

    @staticmethod
    def to_float(value):
        try:
            return float(value)
        except ValueError:
            return 0.00
