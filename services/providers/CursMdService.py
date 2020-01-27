import re

import config

from services.ParseService import ParseService


class CursMdService(ParseService):
    def __enter__(self):
        self.set_url(config.URL)
        self.set_exclusion(config.EXCLUSION)
        return self.start()

    def extract_data(self, soup):
        try:
            result = soup.find('table', id=config.SEARCH_FOR_ID) \
                .find('tbody') \
                .findAll('tr')
        except Exception as err:
            raise err
        else:
            return result

    def to_dictionary(self):
        try:
            banks = {}
            for raw in self.get_data():
                key = raw['class'][0]

                if key in self.get_exclusion():
                    continue

                a = raw.findAll('td')[0].find('a')
                banks[key] = {}
                banks[key]['title'] = a.get_text().strip()
                banks[key]['address'] = a['title']
                banks[key]['currencies'] = {}

                for td in raw.findAll('td'):
                    match = re.search(r'([A-Z])\w+', td['class'][0])

                    if not match:
                        continue

                    currency = match.group(0).upper()
                    rate = self.to_float(td.get_text())

                    if currency not in banks[key]['currencies']:
                        banks[key]['currencies'][currency] = {}
                        banks[key]['currencies'][currency]['buy'] = rate
                    else:
                        banks[key]['currencies'][currency]['sell'] = rate

        except TypeError as type_err:
            raise type_err
        else:
            return banks
