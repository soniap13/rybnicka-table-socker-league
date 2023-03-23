


def is_float(text: str) -> bool:
    return text.replace('.', '', 1).isnumeric()
