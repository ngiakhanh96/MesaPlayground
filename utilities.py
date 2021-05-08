def is_equal_pos(pos1, pos2):
    if (pos1 is None and pos2 is None):
        return True
    if (pos1 is None or pos2 is None):
        return False
    if (pos1[0] == pos2[0] and pos1[1] == pos2[1]):
        return True
    return False


def get_spot_pos_list():
    return list(
        map(
            convert_string_to_tuple_pos,
            get_spot_pos_dict().values()))


def convert_string_to_tuple_pos(spot_pos_str):
    return tuple(
        map(lambda x: int(x), spot_pos_str.split(",")))


def get_spot_pos_dict():
    return {"0": "3,1", "1": "3,3", "2": "3,5",
            "3": "6,5", "4": "6,3", "5": "6,1"}


def get_product_pos_dict():
    return {"0": None, "1": "3,2", "2": "3,4",
            "3": "6,6", "4": "6,4", "5": "6,2"}


def convert_spot_pos_to_product_pos(position):
    x, y = position
    if (x == 6):
        return (x, y+1)
    if (x == 3 and y != 1):
        return (x, y - 1)
    return None


def convert_spot_pos_to_next_product_pos(position):
    spot_dict = get_spot_pos_dict()
    x, y = position
    for i in spot_dict.keys():
        if (int(i) < len(spot_dict.keys()) - 1):
            if (spot_dict[i] == str(x) + "," + str(y)):
                next_pos = get_spot_pos_from_dict(str(int(i)+1))
                return convert_spot_pos_to_product_pos(next_pos)
        else:
            return None


def get_spot_pos_from_dict(key):
    spot_pos_str = get_spot_pos_dict()[key]
    return convert_string_to_tuple_pos(spot_pos_str)
