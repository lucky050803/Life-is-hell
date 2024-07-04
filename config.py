import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def save_config(config):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
