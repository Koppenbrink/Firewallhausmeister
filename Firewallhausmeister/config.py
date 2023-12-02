import json
import os,sys
from helper import config_location


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

config_loc = resource_path(config_location)
# functions
def save_config():
    json.dump(config, open(config_loc, 'w'))

def change_config(key, value):
    config[key] = value
    save_config()

# load config
def load_config():
    config = json.load(open(config_loc))
    return config


settings_button_dict = {}
config = load_config()