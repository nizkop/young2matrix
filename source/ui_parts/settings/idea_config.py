import json

CONFIG_FILE = './source/ui_parts/settings/language_config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {}
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def update_language(language):
    config = load_config()
    config['language'] = language
    save_config(config)

def get_language():
    config = load_config()
    return config.get('language', 'default_language')


if __name__ == '__main__':
    update_language('de')
    # update_language('en')
    print(get_language())
