from math import *

def get_data_back(path_for_file):
    f = open(path_for_file)
    read = f.read()
    returned_to_dict_form = eval(read)
    return returned_to_dict_form

class Datapoint(object):

    def __init__(self, x, y, timeStamp):
        self.x = x
        self.y = y
        self.timeStamp = timeStamp

    @classmethod
    def from_json(cls, json_str):
        # takes the json string, unpacks it as data
        data = json.loads(json_str)

        # takes the data, turns each dictionary into an object instead
        # puts the objects into a list called points
        points = [ cls(pt['x'], pt['y'], pt['timestamp']) for pt in data]
        return points

    # __str__ will give the string version of objects.  
    # Since two things could be identical, it would overwrite;
    # __repr__ gives a unique representation of the objects within
    def __repr__(self):
        return "DataPoint(%d, %d, %d)" % (self.x, self.y, self.timeStamp)

def closest_letter(chosen_point):
    keyboard = get_data_back('seed_data/user_keyboard.txt')
    best_distance = 1,000
    choice_letter = None
    for letter in keyboard:
    # which key center is closest?
        distance = pow((chosen_point['x'] - letter['x']), 2) + pow((chosen_point['y'] - letter['y']), 2)
        if distance < best_distance:
            best_distance = distance
            choice_letter = letter['letter']
    return (choice_letter, best_distance)



# create swipe class for these things
def curve_smoothing():
    data_dicts = get_data_back('seed_data/swipe_objects.txt')
    smoothed_points = []
    first_point = data_dicts[0]
    smoothed_points.append(first_point)
    i = 1
    end = len(data_dicts) - 1
    smoothed_point = {}

    while i < end:
        previous_point = data_dicts[i - 1]
        next_point = data_dicts[i + 1]
        current_point = data_dicts[i]
        # print "previous %r current %r next point: %r" % (previous_point, current_point, next_point)

        smoothed_x = float((current_point['x'] + previous_point['x'] + next_point['x'])) / 3
        smoothed_y = float((current_point['y'] + previous_point['y'] + next_point['y'])) / 3
        # print "smoothed x : %r.  smoothed y: %r" % (smoothed_x, smoothed_y)

        timestamp = current_point['timestamp']
        smoothed_point = {'x': smoothed_x, 'y': smoothed_y, 'timestamp': timestamp}

        smoothed_points.append(smoothed_point)
        # print "smoothed points %r" % smoothed_points
        i = i + 1
    last_point = data_dicts[-1]
    smoothed_points.append(last_point)
    return smoothed_points

def letters_path_crosses():
    swipe_objects = get_data_back('seed_data/swipe_objects.txt')

    # smooth_data_dicts = curve_smoothing()
    letters_crossed = []
    for point in swipe_objects:
        best_letter_guess = closest_letter(point)
        letter = best_letter_guess[0]
        if len(letters_crossed) == 0:
            letters_crossed.extend(letter)
        elif letters_crossed[-1] == letter:
            continue
        else:
            letters_crossed.extend(letter)
    # print letters_crossed
    return letters_crossed

def starting_letter():
    swipe_objects = get_data_back('seed_data/swipe_objects.txt')
    #this may not be necessary because  the list is ordered already
    swipe_in_time_order = sorted(swipe_objects, key=lambda x: x['timestamp'])
    first_point = swipe_in_time_order[0]
    first_letter_info = closest_letter(first_point)
    return first_letter_info


def ending_letter():
    swipe_objects = get_data_back('seed_data/swipe_objects.txt')
    # this may not be necessary because  the list is ordered already
    swipe_in_time_order = sorted(swipe_objects, key=lambda x: x['timestamp'])
    ending_point = swipe_in_time_order[-1]
    last_letter_info = closest_letter(ending_point)
    return last_letter_info

def guess_bigram():
    start = starting_letter()
    end = ending_letter()
    letters = [start, end]
    return letters
    # return bigram, make sure you send it to the browser

def get_vector_list():
    # smoothed_curve = curve_smoothing()
    swipe_objects = get_data_back('seed_data/swipe_objects.txt')

    i = 0
    # end = len(smoothed_curve)-1
    end = len(swipe_objects)-1

    vector_list = []

    while i < end:
        # next_point = smoothed_curve[i + 1]
        # current_point = smoothed_curve[i]
        next_point = swipe_objects[i + 1]
        current_point = swipe_objects[i]
# when I was using curve smoothing, it made sense to have a float here.
        # vector1x = float(next_point['x'] - current_point['x'])
        # vector1y = float(next_point['y'] - current_point['y'])

        vector1x = next_point['x'] - current_point['x']
        vector1y = next_point['y'] - current_point['y']
        # print "current x: %d next x: %d current y: %d next y: %d" % (current_point['x'], next_point['x'], current_point['y'], next_point['y'])
        # print "This is the diff between xes: %d and ys %d" % (vector1x, vector1y)
        # print vector1x.__class__
        # print vector1y.__class__

        vector_magnitude = float(sqrt(vector1x**2 + vector1y**2))
        timestamp = current_point['timestamp']
        # print "This is the vector magnitude: %r and this is the timestamp %r" % (vector_magnitude, timestamp)
        unitx = float(vector1x / vector_magnitude)
        unity = float(vector1y / vector_magnitude)
        # print "This is unitx: %r and this is unity: %r" % (unitx, unity)
        unit_vector = {'unitx': unitx, 'unity': unity, 'x1': current_point['x'], 'x2': next_point['x'],\
                       'y1': current_point['y'], 'y2': next_point['y'], 'timestamp1': timestamp,\
                       'timestamp2': next_point['timestamp']}
        # print "This is the unit vector: %r" % unit_vector
        vector_list.append(unit_vector)
        i = i + 1
    # print vector_list
    return vector_list

def get_thetas():
    vectors = get_vector_list()
    i = 0
    end = len(vectors) - 1
    list_of_thetas_and_time = []
    vectors_angles_xs_ys_timestamps = []

    while i < end:
        current_vector = vectors[i]
        next_vector = vectors[i+1]
        x1 = current_vector['unitx']
        y1 = current_vector['unity']
        x2 = next_vector['unitx']
        y2 = next_vector['unity']
        # print 'CURRENT vector x: %r current vector y: %r next vector x: %r next vector y: %r' % (x1, y1, x2, y2)
        start_time = current_vector['timestamp1']
        # list_of_start_times.append(start_time)
        # print start_time

        cos_of_the_angle = x1*x2 + y1*y2
        # accounts for float errors that would make arccos greater than 1
        if cos_of_the_angle > 1:
            cos_of_the_angle = 1
        # print "Cos of the angle is: %r for x1: %r x2: %r y1: %r y2: %r" % (cos_of_the_angle, x1, x2, y1, y2)
        angle_in_radians = acos(cos_of_the_angle)
        # print "angle in radians: %r" % angle_in_radians
        angle_in_degrees = angle_in_radians * 180 / pi
        # print "angle in degrees: %r" % angle_in_degrees

        # list_of_angles.append(angle_in_degrees)
        # print "radians: %s degrees: %r" % (angle_in_radians, angle_in_degrees)
        # print angle_in_degrees
        angle_info = [start_time, angle_in_degrees]
        vector_angle_x_y_timestamp = {'vector1': current_vector, 'vector2': next_vector, 'angle': angle_in_degrees}
        list_of_thetas_and_time.append(angle_info)
        vectors_angles_xs_ys_timestamps.append(vector_angle_x_y_timestamp)
        i = i + 1
    # print list_of_start_times
    # print list_of_angles
    print list_of_thetas_and_time
    return vectors_angles_xs_ys_timestamps

def get_change_points():
    time_comma_angle_list = get_thetas()
    list_of_change_points = []
    
    max_angle = 0
    peak = None

    for item in time_comma_angle_list:
        if item['angle'] > 20 and item['angle'] > max_angle:
            max_angle = item['angle']
            peak = item
            # print "this angle was greater than 15 and greater than max %r" % max_angle
        elif item['angle'] < max_angle:
            list_of_change_points.append(peak)
            # print "this is the point that was added %r" % peak
            max_angle = 0
            peak = None
        else:
            continue

    # print "this is the list of changed points %r" % list_of_change_points
    return list_of_change_points

def get_change_point_letters():
    change_points = get_change_points()
    change_points_and_letter = []
    for item in change_points:
        vector1 = item['vector1']
        x = vector1['x2']
        y = vector1['y2']
        timestamp = vector1['timestamp2']
        point_data = {'x': x, 'y': y, 'timestamp': timestamp}
        letter = closest_letter(point_data)
        # print letter
        important_point_and_letter = [letter, point_data]
        change_points_and_letter.append(important_point_and_letter)
    # print "this is the changed points and letter %r" % change_points_and_letter
    return change_points_and_letter

def put_word_together():
    letter_and_point_data = get_change_point_letters()
    start = starting_letter()
    start_letter = start[0]
    letters = [start_letter]
    letter_data = [start]
    end = ending_letter()
    end_letter = end[0]
    # print "start letter: %r end letter: %r" % (start_letter, end_letter)
    for point in letter_and_point_data:
        letter_info = point[0]
        letter = letter_info[0]
        if letter != letters[-1]: 
            letters.extend(letter)
            letter_data.extend(letter_info)
        elif letter == letters[-1]:
            continue
    if letters[-1] != end_letter:
        letter_data.extend(end)
        letters.extend(end_letter)
    # print letters
    word = "".join(letters)
    print word
    return word


# if the user looped on a letter (LL, OO, EE, RR, TT, PP, SS, DD, FF, GG, CC, BB, NN, MM)
# add the double letter back in-- 
# look at timestamps and if the user was on that letter 2x as long as usual for the swipe.