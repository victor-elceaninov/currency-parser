import json

import config

from services.BanksService import BanksService
from services.providers.CursMdService import CursMdService


def from_json(currency, offer_type):
    banks_service = BanksService(
        CursMdService(),
    )

    try:
        with open('banks.json') as json_data:
            data = json.loads(json_data.read())
        banks_service.set_banks(data)
        best_rate = banks_service.get_best_rate(currency, offer_type)
    except Exception as err:
        banks_service.display_error(err)
    else:
        banks_service.display('greetings')
        print(best_rate)


from_json('USD', config.OFFER_TYPES[0])
