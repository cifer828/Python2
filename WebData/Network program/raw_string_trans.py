transfer = {'\n': r'\n', '\r':r'\r'}
def raw_string(str):
    """
    :param str: string
    :return: raw string
    """
    new_str = ''
    for char in str:
        try:
            new_str += transfer[char]
        except KeyError:
            new_str += char
    return new_str

# s = '\nafsafasfasfs\rfasdfsfsa\nafdasff'
# print raw_string(s)