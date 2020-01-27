import sys

import config
from validators.BankValidator import Bank
from services.MessagesService import MessagesService
from services.ParseService import ParseService


class BanksService:
    __banks = {}
    __currencies = []
    __best_rate = 0.00
    __inserted_type = 0
    __inserted_currency = 0
    __offer_types = config.OFFER_TYPES
    __best_rate_banks = []

    def __init__(self, parse_service: ParseService):
        self.__messages_service = MessagesService()
        self.__parse_service = parse_service

    def init(self):
        try:
            self.set_banks(self.__get_all_banks())
        except Exception as err:
            self.display_error(err)
        else:
            self.__initiate_interface()

    def set_banks(self, banks):
        with Bank(banks):
            self.__banks = banks
            self.__generate_currency_list()

    def get_banks(self):
        return self.__banks

    def get_currencies(self):
        if self.__validate_banks():
            return self.__currencies
        return None

    def get_best_rate(self, currency, offer_type):
        if self.__validate_banks():
            if self.__best_rate_banks:
                return self.__best_rate_banks
            else:
                return self.__detect_best_rate(currency.upper(), offer_type)
        return None

    def __detect_best_rate(self, currency, offer_type):
        for key, bank in self.get_banks().items():
            try:
                bank_currency = bank['currencies'][currency][offer_type]
            except KeyError as key_err:
                self.display_error(key_err)
                return None
            else:
                if offer_type == self.__offer_types[0]:
                    if bank_currency > self.__best_rate:
                        self.__best_rate = bank_currency
                        self.__best_rate_banks = [bank]
                    elif bank_currency == self.__best_rate:
                        self.__best_rate_banks.append(bank)
                else:
                    if bank_currency < self.__best_rate \
                            or self.__best_rate == 0:
                        self.__best_rate = bank_currency
                        self.__best_rate_banks = [bank]
                    elif bank_currency == self.__best_rate:
                        self.__best_rate_banks.append(bank)

        if self.__best_rate_banks:
            return self.__best_rate_banks
        return None

    def __get_all_banks(self):
        with self.__parse_service as banks:
            return banks

    def __generate_currency_list(self):
        banks = self.get_banks()
        currencies_dic = next(iter(banks.values()))['currencies']
        for currency, value in currencies_dic.items():
            self.__currencies.append(currency)

    def __validate_banks(self):
        if not self.__banks:
            self.display('banks_requires')
            return None
        return True

    def __initiate_interface(self):
        self.display('greetings')
        self.display('choose_offer_type')

        self.__inserted_type = self.__make_choice(self.__offer_types)

        self.display('all_currencies')
        self.__inserted_currency = self.__make_choice(self.get_currencies())

        self.__handler()

    def __make_choice(self, data):
        self.__messages_service.print_numeric_list(data)
        while True:
            self.display('insert_number')
            insertion = sys.stdin.readline()
            if self.__input_validation(insertion, data) is True:
                choice = int(insertion) - 1
                break

        self.display('your_choice', data[choice])
        return data[choice]

    @staticmethod
    def __input_validation(request, arguments):
        try:
            result = int(request)
        except ValueError:
            return None
        else:
            if result in range(1, len(arguments) + 1):
                return True

    def __handler(self):
        offer_type = self.__inserted_type
        currency = self.__inserted_currency
        self.__detect_best_rate(currency, offer_type)

        self.display('best_rate', self.__best_rate)
        for bank in self.__best_rate_banks:
            self.display('full_info', bank['title'], bank['address'])

    def display(self, message, *arguments):
        self.__messages_service.display(message, *arguments)

    def display_error(self, err):
        self.display('error', type(err).__name__, str(err))
