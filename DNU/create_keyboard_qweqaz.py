def get_data_back(path_for_file):
    f = open(path_for_file)
    read = f.read()
    returned_to_dict_form = eval(read)
    return returned_to_dict_form

def get_key_center():
    # finds the average x and y to be the center of the letter
    calibration_dictionary = get_data_back('seed_data/swipe_calibration.txt')
    key_center_list = []
    for letter_values in calibration_dictionary:
        xvalues = []
        yvalues = []
        coordinates = letter_values[1]
# coordinates is a list containing tuples
        letter_sublist = letter_values[0]
        # letter is in the form [u'q']
        letter = letter_sublist[0]
        for coordinate in coordinates:
# coordinate is a tuple of 3 values- x, y, and timestamp
            xvalues.append(coordinate[0])
            yvalues.append(coordinate[1])

        average_x = float(sum(xvalues)/len(xvalues))
        average_y = float(sum(yvalues)/len(yvalues))
        key_location = {'letter':letter, 'x':average_x, 'y':average_y}
        key_center_list.append(key_location)
    return key_center_list

def q_location():
    training_keys = get_key_center()
    q1 = training_keys[0]
    q2 = training_keys[3]
    average_q_x = (q1['x'] + q2['x'])/2
    average_q_y = (q1['y'] + q2['y'])/2
    q = {'letter':'q', 'x':average_q_x, 'y':average_q_y}
    return q

def keyboard_map():
    training_keys = get_key_center()
    row_1 = ['r', 't', 'y', 'u', 'i', 'o', 'p'] # preceded by q, w, e
    row_2 = ['s', 'd', 'f', 'g', 'h', 'j', 'k', 'l'] # preceded by a
    row_3 = ['x', 'c', 'v', 'b', 'n', 'm'] # preceded by z
    q = q_location()
    w = training_keys[1]
    e = training_keys[2]
    a = training_keys[4]
    z = training_keys[5]
    
    keyboard = [q, w, e, a, z]

    horizontal_key_distance = ((w['x'] - q['x']) + (e['x'] - w['x'])) / 2
    vertical_key_distance = ((z['y'] - a['y']) + (a['y'] - q['y'])) / 2
    
    average_row_1_y = (q['y'] + w['y'] + e['y']) / 3
    average_row_2_y = average_row_1_y + vertical_key_distance
    average_row_3_y = average_row_2_y + vertical_key_distance

    initial_x = e['x']
    for letter in row_1:
        letter_info = {}
        letter_info['letter'] = letter
        letter_info['x'] = initial_x + horizontal_key_distance
        letter_info['y'] = average_row_1_y
        keyboard.append(letter_info)
        initial_x = letter_info['x']

    initial_x = a['x']
    for letter in row_2:
        letter_info = {}
        letter_info['letter'] = letter
        letter_info['x'] = initial_x + horizontal_key_distance
        letter_info['y'] = average_row_2_y
        keyboard.append(letter_info)
        initial_x = letter_info['x']

    initial_x = z['x']
    for letter in row_3:
        letter_info = {}
        letter_info['letter'] = letter
        letter_info['x'] = initial_x + horizontal_key_distance
        letter_info['y'] = average_row_3_y
        keyboard.append(letter_info)
        initial_x = letter_info['x']
    print keyboard

    f = open('seed_data/user_keyboard.txt', 'w')
    # change to mode 'a' if you want to append instead of overwrite
    string_keyboard = str(keyboard)
    f.write(string_keyboard)
    f.close()
    return keyboard
    ##### note--- i'll have to account for the spacebar somehow.
