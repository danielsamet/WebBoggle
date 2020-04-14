import uuid


def base36encode(integer):
    """code attribution - https://en.wikipedia.org/wiki/Base36 as of 04/07/2019"""

    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    sign = '-' if integer < 0 else ''
    integer = abs(integer)
    result = ''

    while integer > 0:
        integer, remainder = divmod(integer, 36)
        result = chars[remainder] + result

    return sign + result


def generate_uuid(length=6):
    return base36encode(uuid.uuid4().int)[:length]
