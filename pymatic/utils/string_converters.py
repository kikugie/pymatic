# Warning boilerplate code
def conv_str(value):
    if value.isdigit():
        return int(value)
    elif value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        return value


def to_str(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, int):
        return str(value)
    else:
        return value
