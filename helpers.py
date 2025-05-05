def get_key_from_dict (dictionary: dict, pos= -1) -> list | str:
    if pos >= 0:
        return list(dictionary.keys())[pos]
    else:
        return list(dictionary.keys())

def get_value_from_dict (dictionary: dict, pos= -1 ) -> list | str:
    if pos >= 0:
        return list(dictionary.values())[pos]
    else:
        return list(dictionary.values())