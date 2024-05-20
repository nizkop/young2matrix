import json

from source.ui_parts.settings.language_choices import language_choices

CONFIG_FILE = './source/ui_parts/settings/language_config.json'

def load_config() -> None:
    """ load the current value of the language from the settings file """
    try:
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {}
    return config

def update_language(language:str) -> None:
    """
    change the current language (in the configuration file, so that the change lasts)
    :param language: abbreviation of the wanted language
    """
    if language not in [language_choices.en.name, language_choices.de.name]:
        raise Exception("wrong format for language choice")
    config = load_config()
    config['language'] = language
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)


def get_language() -> str:
    """ get current language
    :return: abbreviation of the current language (in case of error: default_language) """
    return load_config()['language']



if __name__ == '__main__':
    update_language('de')
    # update_language('en')
    print(get_language())