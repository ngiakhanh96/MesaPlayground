import numpy
left_x_pos_spot_column = 3
right_x_pos_spot_column = 6

spot_pos_dict_conf = {"0": (left_x_pos_spot_column,  1), "1": (left_x_pos_spot_column,  3), "2": (left_x_pos_spot_column,  5),
                      "3": (right_x_pos_spot_column, 5), "4": (right_x_pos_spot_column, 3), "5": (right_x_pos_spot_column, 1)}

product_processing_duration_dict_input_conf = {"0": {"A": [1], "B": [1,2]}, "1": {"A": [1], "B": [1]}, "2": {"A": [1], "B": [1]},
                                               "3": {"A": [1], "B": [1]}, "4": {"A": [1], "B": [1]}, "5": {"A": [1], "B": [1]}}

agv_station_pos_dict_conf = {"0": (4, 7), "1": (5, 7)}

def get_product_processing_duration_dict():
    product_processing_duration_dict = {}
    for key,value in product_processing_duration_dict_input_conf.items():
        for product_name,product_processing_duration_arr in value.items():
            product_processing_duration = None
            product_processing_duration_arr_length = len(product_processing_duration_arr)
            if (product_processing_duration_arr_length > 2):
                product_processing_duration = numpy.random.triangular(
                    product_processing_duration_arr[0], 
                    product_processing_duration_arr[1], 
                    product_processing_duration_arr[2])
            elif (product_processing_duration_arr_length > 1):    
                product_processing_duration = numpy.random.uniform(
                    product_processing_duration_arr[0], 
                    product_processing_duration_arr[1])
            else:
                product_processing_duration = product_processing_duration_arr[0]
            if key not in product_processing_duration_dict:
                product_processing_duration_dict[key] = {}
            product_processing_duration_dict[key][product_name] = round(product_processing_duration)
    return product_processing_duration_dict
product_processing_duration_dict_conf = get_product_processing_duration_dict()


def get_product_pos_dict():
    product_pos_dict = {}
    spot_pos_dict = spot_pos_dict_conf
    first_spot_pos_key = list(spot_pos_dict.keys())[0]
    for key,spot_pos in spot_pos_dict.items():
        if spot_pos[0] == left_x_pos_spot_column:
            product_pos_dict[key] = None if key == first_spot_pos_key else (left_x_pos_spot_column, spot_pos[1] - 1)
        else:
            product_pos_dict[key] = (right_x_pos_spot_column, spot_pos[1] + 1)
    return product_pos_dict
product_pos_dict_conf = get_product_pos_dict()


def get_left_kanban_pos_dict():
    left_kanban_pos_dict = {}
    spot_pos_dict = spot_pos_dict_conf
    for key,spot_pos in spot_pos_dict.items():
        if spot_pos[0] == left_x_pos_spot_column:
            left_kanban_pos_dict[key] = (left_x_pos_spot_column - 1, spot_pos[1])
    return left_kanban_pos_dict
left_kanban_pos_dict_conf = get_left_kanban_pos_dict()


def get_right_kanban_pos_dict():
    right_kanban_pos_dict = {}
    spot_pos_dict = spot_pos_dict_conf
    for key,spot_pos in spot_pos_dict.items():
        if spot_pos[0] == right_x_pos_spot_column:
            right_kanban_pos_dict[key] = (right_x_pos_spot_column + 1, spot_pos[1])
    return right_kanban_pos_dict
right_kanban_pos_dict_conf = get_right_kanban_pos_dict()


def get_filling_pos_dict():
    filling_pos_dict = {}
    spot_pos_dict = spot_pos_dict_conf
    for key,spot_pos in spot_pos_dict.items():
        if spot_pos[0] == left_x_pos_spot_column:
            filling_pos_dict[key] = (left_x_pos_spot_column - 2, spot_pos[1])
        else:
            filling_pos_dict[key] = (right_x_pos_spot_column + 2, spot_pos[1])
    return filling_pos_dict
filling_pos_dict_conf = get_filling_pos_dict()
