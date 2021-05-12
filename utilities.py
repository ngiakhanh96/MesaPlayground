def get_spot_pos_dict():
    return {"0": (3, 1), "1": (3, 3), "2": (3, 5),
            "3": (6, 5), "4": (6, 3), "5": (6, 1)}


def get_product_pos_dict():
    return {"0": None, "1": (3, 2), "2": (3, 4),
            "3": (6, 6), "4": (6, 4), "5": (6, 2)}


def get_kanban_pos_dict():
    return {**get_left_kanban_pos_dict(), **get_right_kanban_pos_dict()}


def get_left_kanban_pos_dict():
    return {"0": (2, 1), "1": (2, 3), "2": (2, 5)}


def get_right_kanban_pos_dict():
    return {"3": (7, 5), "4": (7, 3), "5": (7, 1)}


def get_agv_station_pos_dict():
    return {"0": (4, 7), "1": (5, 7)}


def convert_kanban_pos_to_filling_pos(kanban_pos, left_or_right):
    kanban_posX, kanban_posY = kanban_pos
    if (left_or_right == "0"):
        kanban_posX -= 1
    else:
        kanban_posX += 1
    return (kanban_posX, kanban_posY)


def convert_spot_pos_to_kanban_pos(spot_pos):
    spot_posX, spot_posY = spot_pos
    if (spot_posX == 3):
        spot_posX -= 1
    else:
        spot_posX += 1
    return (spot_posX, spot_posY)


def convert_spot_pos_to_product_pos(position):
    x, y = position
    if (x == 6):
        return (x, y + 1)
    if (x == 3 and y != 1):
        return (x, y - 1)
    return None


def get_spot_pos_list():
    return list(get_spot_pos_dict().values())


def get_kanban_pos_list():
    return list(get_kanban_pos_dict().values())


def is_equal_pos(pos1, pos2):
    if (pos1 is None and pos2 is None):
        return True
    if (pos1 is None or pos2 is None):
        return False
    if (pos1[0] == pos2[0] and pos1[1] == pos2[1]):
        return True
    return False


# def convert_string_to_tuple_pos(spot_pos_str):
#     return tuple(
#         map(lambda x: int(x), spot_pos_str.split(",")))


def convert_spot_pos_to_next_product_pos(position):
    spot_dict = get_spot_pos_dict()
    for i in spot_dict.keys():
        if (int(i) < len(spot_dict.keys()) - 1):
            if (is_equal_pos(spot_dict[i], position)):
                next_pos = get_spot_pos_from_dict(str(int(i)+1))
                return convert_spot_pos_to_product_pos(next_pos)
        else:
            return None


def get_spot_pos_from_dict(key):
    return get_spot_pos_dict()[key]


def get_kanban_pos_from_dict(key):
    return get_kanban_pos_dict()[key]


def get_agv_station_pos_from_dict(key):
    return get_agv_station_pos_dict()[key]
