import configparser

_config = configparser.ConfigParser()
_config.read('s3_project/Config/config.ini')


def find_variable(variable, location='BUCKET'):
    return _config[location][variable]
