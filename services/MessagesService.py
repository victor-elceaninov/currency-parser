import messages


class MessagesService:
    def __init__(self):
        self.messages = messages.MSG

    def display(self, key, *arguments):
        if key not in self.messages:
            raise Exception(self.messages['key_not_exists'])

        if not all(arguments):
            arguments = ()
        try:
            print((self.messages[key]).format(*arguments))
        except TypeError as type_err:
            raise type_err
        except Exception as err:
            raise err

    def print_numeric_list(self, data):
        for index, raw in enumerate(data):
            index += 1
            self.display('print_list', index, raw)
