from source.ui_parts.settings.settings_config import get_color


def get_scrollbar_colors(kind:str):
    color = get_color()
    return rf"""
                QScrollBar:{kind} {{
                    background: {color['background']};;
                }}
                QScrollBar::handle:{kind} {{
                    background: {color['status_background']};
                    margin: {'15px 1px 15px 1px' if kind == 'vertical' else '1px 15px 1px 15px'};  /* top, right, bottom, left */
                }}
            """