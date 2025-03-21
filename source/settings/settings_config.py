import json

from source.settings.ColorStyles import ColorStyles
from source.settings.GLOBALS import FILE_PATH_CONFIG_FILE
from source.settings.LanguageChoices import LanguageChoices



def load_config() -> None:
    """ load the current value of the language from the settings file """
    try:
        with open(FILE_PATH_CONFIG_FILE, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:#default
        config = {"language": "en", "color": "PLAIN"}#<- changeable in UI
    return config

def update_settings(new_input:str, key:str) -> None:
    """
    change the current language (in the configuration file, so that the change lasts)
    :param new_input: abbreviation of the wanted language/color
    :param key: key to save the new value in the settings dict
    """
    if key == "language":
        if new_input not in [language.name for language in LanguageChoices]:
            raise Exception(f"wrong format for language choice")
    elif key == "color":
        if new_input not in [c.name for c in ColorStyles]:
            raise Exception(f"wrong format for color scheme choice")
    else:
        raise Exception("unknown key for settings")
    config = load_config()
    config[key] = new_input
    with open(FILE_PATH_CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def get_language() -> str:
    """ short version to get current language
    safety for exception (key error) in load_config
    :return: abbreviation of the current language (in case of error: default_language) """
    return load_config()['language']

def get_color() -> dict:
    """
    short version to get the color settings
    safety for exception (key error) in load_config
    :return: dict value containing all information about the actual color scheme
    """
    settings = load_config()
    return ColorStyles[settings['color']].value
