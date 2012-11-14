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
    q = q_location()
    t = training_keys[1]
    p = training_keys[2]
    a = training_keys[4]
    z = training_keys[5]
    keyboard = [q, t, p, a, z]

    row_1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'backspace']
    row_2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
    row_3 = ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma', 'period', 'shift']

    full_spread_average = (p['x'] - q['x']) / 9
    four_key_spread_average = (t['x'] - q['x']) / 4
    horizontal_key_distance = (full_spread_average + four_key_spread_average) / 2
    vertical_key_distance = ((z['y'] - a['y']) + (a['y'] - q['y'])) / 2
    
    average_row_1_y = (q['y'] + t['y'] + p['y']) / 3
    average_row_2_y = average_row_1_y + vertical_key_distance
    average_row_3_y = average_row_2_y + vertical_key_distance

    initial_x = q['x']
    for letter in row_1:
        if letter == 'q' or letter == 'p':
            continue
        elif letter == 't':
            initial_x = t['x']
        else:
            new_letter = create_new_letter_dict(letter, initial_x, average_row_1_y, horizontal_key_distance, keyboard)
            initial_x = new_letter['x']

    initial_x = a['x']
    for letter in row_2:
        if letter == 'a':
            continue
        else:
            new_letter = create_new_letter_dict(letter, initial_x, average_row_2_y, horizontal_key_distance, keyboard)
            initial_x = new_letter['x']

    initial_x = z['x']
    for letter in row_3:
        if letter == 'z':
            continue
        else:
            new_letter = create_new_letter_dict(letter, initial_x, average_row_3_y, horizontal_key_distance, keyboard)
            initial_x = new_letter['x']
    # for key in keyboard:
        # print "letter: %s x: %d y: %d" % (key['letter'], key['x'], key['y'])
    f = open('seed_data/user_keyboard.txt', 'w')
    # change to mode 'a' if you want to append instead of overwrite
    string_keyboard = str(keyboard)
    f.write(string_keyboard)
    f.close()
    return keyboard
    ##### note--- i'll have to account for the spacebar somehow.

    
def create_new_letter_dict(letter, initial_x, row_number_y_height, horizontal_key_distance, keyboard):
    letter_info = {}
    letter_info['letter'] = letter
    letter_info['x'] = initial_x + horizontal_key_distance
    letter_info['y'] = row_number_y_height
    keyboard.append(letter_info)
    return letter_info

