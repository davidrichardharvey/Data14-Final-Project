import configparser

_config = configparser.ConfigParser()
_config.read('Config/config.ini')


def find_variable(variable, location='BUCKET'):
    return _config[location][variable]
