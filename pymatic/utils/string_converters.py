# Warning boilerplate code
def to_str(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, int):
        return str(value)
    else:
        return value


def parse_str(s: str, /):
    if s.isdigit():
        return int(s)
    elif s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        return str(s)
