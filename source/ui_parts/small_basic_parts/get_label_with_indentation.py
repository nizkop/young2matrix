from source.settings.GLOBALS import BUTTON_SIZE, MARGIN_TOP_Y


def get_label_with_indentation(label:str) -> str:
    """
    move ui labels a bit to the right (e.g. to show they are a sub part of what stands above them)
    :param label: content of Qlabel to-be
    :return: content with indentation (as html format)
    """
    content = f"<p>{label}</p>"
    spacer_height = BUTTON_SIZE + 2 * MARGIN_TOP_Y
    return f"<div style='margin-left: {1.8*spacer_height}px;'>{content}</div>"
