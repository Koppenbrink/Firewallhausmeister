import json

# functions
def save_config():
    json.dump(config, open("config.txt",'w'))

def change_config(key, value):
    config[key] = value
    save_config()

# load config
def load_config():
    config = json.load(open("config.txt"))
    return config
    # load settings
    direction = config['direction']

config = load_config()



