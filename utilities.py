from configuration import *

def get_spot_pos_from_dict(key):
    return spot_pos_dict_conf[key]


def get_kanban_pos_from_dict(key):
    return get_kanban_pos_dict[key]


def get_agv_station_pos_from_dict(key):
    return agv_station_pos_dict_conf[key]


get_kanban_pos_dict = {**left_kanban_pos_dict_conf, **right_kanban_pos_dict_conf}


get_spot_pos_list = list(spot_pos_dict_conf.values())


get_kanban_pos_list = list(get_kanban_pos_dict.values())


def is_equal_pos(pos1, pos2):
    if (pos1 is None and pos2 is None):
        return True
    if (pos1 is None or pos2 is None):
        return False
    if (pos1[0] == pos2[0] and pos1[1] == pos2[1]):
        return True
    return False


def convert_spot_pos_to_kanban_pos(spot_pos):
    spot_pos_dict = spot_pos_dict_conf
    index = find_pos_index_in_dict(spot_pos, spot_pos_dict)
    return None if index is None else get_kanban_pos_dict[index]


def convert_spot_pos_to_product_pos(spot_pos):
    spot_pos_dict = spot_pos_dict_conf
    index = find_pos_index_in_dict(spot_pos, spot_pos_dict)
    return None if index is None else product_pos_dict_conf[index]


def convert_spot_pos_to_next_product_pos(spot_pos):
    spot_pos_dict = spot_pos_dict_conf
    product_pos_dict = product_pos_dict_conf
    index = find_pos_index_in_dict(spot_pos, spot_pos_dict)
    if index is None:
        return None
    index_list = list(spot_pos_dict.keys())
    order_in_index_list = index_list.index(index)
    next_order_in_index_list = order_in_index_list + 1
    if next_order_in_index_list > len(index_list) - 1:
        return None
    return product_pos_dict[index_list[next_order_in_index_list]]


def convert_kanban_pos_to_filling_pos(kanban_pos):
    kanban_pos_dict = get_kanban_pos_dict
    index = find_pos_index_in_dict(kanban_pos, kanban_pos_dict)
    return None if index is None else filling_pos_dict_conf[index]


def find_pos_index_in_dict(pos, pos_dict):
    for i in pos_dict.keys():
        if (is_equal_pos(pos_dict[i], pos)):
            return i
    return None

# def convert_string_to_tuple_pos(spot_pos_str):
#     return tuple(
#         map(lambda x: int(x), spot_pos_str.split(",")))
