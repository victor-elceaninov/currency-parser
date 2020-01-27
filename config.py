URL = 'https://www.curs.md/en/curs_valutar_banci'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ('
                  'KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 '
}

PARSER = 'html.parser'

SEARCH_FOR_ID = 'tabelBankValute'

OFFER_TYPES = ('buy', 'sell')

EXCLUSION = ('bnm',)
