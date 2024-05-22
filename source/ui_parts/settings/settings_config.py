import json

from source.ui_parts.settings.color_styles import color_styles
from source.ui_parts.settings.language_choices import language_choices

CONFIG_FILE = './source/ui_parts/settings/config.json'

def load_config() -> None:
    """ load the current value of the language from the settings file """
    try:
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:#default
        config = {"language": "en", "color": "DEFAULT",#<- changeable in UI
                  "font-size": 15, "button-font-size": 20, "margin-top-y": 10, "button-size": 50, "geometry": [100, 100, 800, 600]}
    return config

def update_settings(new_input:str, key:str) -> None:
    """
    change the current language (in the configuration file, so that the change lasts)
    :param new_input: abbreviation of the wanted language/color
    :param key: key to save the new value in the settings dict
    """
    if key == "language":
        if new_input not in [language.name for language in language_choices]:
            raise Exception(f"wrong format for language choice")
    elif key =="color":
        if new_input not in [c.name for c in color_styles]:
            print(new_input)
            raise Exception(f"wrong format for color scheme choice")
    config = load_config()
    config[key] = new_input
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def get_language() -> str:
    """ short verstion to get current language
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
    return color_styles[settings['color']].value
