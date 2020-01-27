class Bank:
    __rules = {
        'title': {
            'type': 'str',
        },
        'address': {
            'type': 'str',
        },
        'currencies': {
            'type': 'dic',
            'child': {
                'buy': {
                    'type': 'float',
                },
                'sell': {
                    'type': 'float',
                },
            }
        },
    }

    def __init__(self, banks):
        self.banks = banks

    def __enter__(self):
        self.validate(self.banks)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise exc_type(exc_val)

    def validate(self, data_, rules=None):
        if rules is None:
            rules = self.__rules

        for item in data_.items():
            for item_key, item_value in item[1].items():
                if self.__validate_field(item_key, item_value, rules):
                    continue
                else:
                    raise IndexError(f'"{item_key}" index doesn\'t exists '
                                     f'in Bank model')
        return True

    def __validate_field(self, item_key, item_value, rules):
        for rule_key, rule in rules.items():
            if item_key == rule_key:
                if not self.__validate_value(item_value, rule):
                    raise TypeError(f'index "{item_key}" with value '
                                    f'"{item_value}" has the wrong data type')
                else:
                    return True
        return None

    def __validate_value(self, value, rule):
        if rule['type'] == 'str' and isinstance(value, str):
            return True
        if rule['type'] == 'float' and isinstance(value, float):
            return True
        elif rule['type'] == 'dic' and isinstance(value, dict):
            return self.validate(value, rule['child'])

        return None
