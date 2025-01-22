db_config = {
    'host': 'sql7.freesqldatabase.com',
    'db': 'sql7750706',
    'port': 3306,
    'user': 'sql7750706',
    'password': '1QqvWs862x'
}

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
encryption_key = config['encryption']['key']


