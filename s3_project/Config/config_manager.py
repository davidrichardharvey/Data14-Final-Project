import configparser

_config = configparser.ConfigParser()
_config.read('Config/config.ini')
_private_config = configparser.ConfigParser()
_private_config.read('Config/private_config.ini')


def find_variable(variable, location='BUCKET'):
    return _config[location][variable]


def find_hidden_variable(variable):
    return _private_config['HIDDEN VARIABLES'][variable]
