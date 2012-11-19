from math import *
def get_data_back(path_for_file):
    f = open(path_for_file)
    read = f.read()
    returned_to_dict_form = eval(read)
    return returned_to_dict_form

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

        smoothed_x = (current_point['x']  + previous_point['x'] + next_point['x']) / 3
        smoothed_y = (current_point['y']  + previous_point['y'] + next_point['y']) / 3
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
    smooth_data_dicts = curve_smoothing()
    letters_crossed = []
    for point in smooth_data_dicts:
        best_letter_guess = closest_letter(point)
        letter = best_letter_guess[0]
        if len(letters_crossed) == 0:
            letters_crossed.extend(letter)
        elif letters_crossed[-1] == letter:
            continue
        else:
            letters_crossed.extend(letter)
    print letters_crossed
    return letters_crossed

def starting_letter():
    swipe_objects = get_data_back('seed_data/swipe_objects.txt')
    #this may not be necessary because  the list is ordered already
    swipe_in_time_order = sorted(swipe_objects, key=lambda x: x['timestamp'])
    first_point = swipe_in_time_order[0]
    first_letter = closest_letter(first_point)
    return first_letter


def ending_letter():
    swipe_objects = get_data_back('seed_data/swipe_objects.txt')
    # this may not be necessary because  the list is ordered already
    swipe_in_time_order = sorted(swipe_objects, key=lambda x: x['timestamp'])
    ending_point = swipe_in_time_order[-1]
    last_letter = closest_letter(ending_point)
    return last_letter

def guess_bigram():
    start = starting_letter()
    end = ending_letter()
    letters = [start, end]
    return letters
    # return bigram, make sure you send it to the browser

def get_vector_list():
    smoothed_curve = curve_smoothing()
    i = 0
    end = len(smoothed_curve)-1
    vector_list = []

    while i < end:
        next_point = smoothed_curve[i + 1]
        current_point = smoothed_curve[i]
        vector1x = float(next_point['x'] - current_point['x'])
        vector1y = float(next_point['y'] - current_point['y'])
        # print "current x: %d next x: %d current y: %d next y: %d" % (current_point['x'], next_point['x'], current_point['y'], next_point['y'])
        # print "This is the diff between xes: %d and ys %d" % (vector1x, vector1y)
        
        vector_magnitude = float(sqrt(vector1x**2 + vector1y**2))
        timestamp = current_point['timestamp']
        # print "This is the vector magnitude: %r and these are the timestamps %r" % (vector_magnitude, timestamps)
        unitx = vector1x / vector_magnitude
        unity = vector1y / vector_magnitude
        # print "This is unitx: %d and this is unity: %d" % (unitx, unity)
        unit_vector = (unitx, unity, timestamp)
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
    list_of_angles = []
    list_of_start_times = []

    while i < end:
        current_vector = vectors[i]
        next_vector = vectors[i+1]
        x1 = current_vector[0]
        y1 = current_vector[1]
        x2 = next_vector[0]
        y2 = next_vector[1]
        # print 'CURRENT vector x: %r current vector y: %r next vector x: %r next vector y: %r' % (x1, y1, x2, y2)
        start_time = current_vector[2]
        # list_of_start_times.append(start_time)
        # print start_time

        cos_of_the_angle = x1*x2 + y1*y2
        angle_in_radians = acos(cos_of_the_angle)
        angle_in_degrees = angle_in_radians * 180 / pi
        # list_of_angles.append(angle_in_degrees)
        # print "radians: %s degrees: %r" % (angle_in_radians, angle_in_degrees)
        # print angle_in_degrees
        angle_info = [start_time, angle_in_degrees]
        list_of_thetas_and_time.append(angle_info)
        i = i + 1
    # print list_of_start_times
    # print list_of_angles
    # print list_of_thetas_and_time
    return list_of_thetas_and_time

def get_change_points():
    time_comma_angle_list = get_thetas()
    list_of_change_points = []
    for item in time_comma_angle_list:
        if item[1] > 11:
            list_of_change_points.append(item)
    print list_of_change_points
    return list_of_change_points

# def get_change_point_letters():
#     change_points_and_letter = []
#     data_dicts = get_data_back('seed_data/swipe_objects.txt')
#     for item in list_of_change_points:
    # letter = closest_letter(chosen_point)

    # get the derivative of theta on a graph
    # see places where it spikes- those are vertices
    # the center of these vertices should be approx the point
    # the letter is one of 7 keys around that point.
    # get the word permutations of each. Save in a list or something.
    # check each of those against the dictionary
def is_it_a_word(bigram):
    pass
    # check dictionary
    # number of vertex points (plus start and end) indicates minimum number of letters
    # is there a word there already?
    # if not, run other function to get slow-down points, or use edit distance, etc

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
    # which point is closest to the chosen point of the bigram?
        distance = float(pow((chosen_point['x'] - letter['x']), 2) + pow((chosen_point['y'] - letter['y']), 2))
        if distance < best_distance:
            best_distance = distance
            choice_letter = letter['letter']
    return (choice_letter, best_distance)


 # figure out which keys fall within a certain
 # margin of error of the value- if you find one that's relatively close, you
 # don't need to check the keys all the way across the board.  That way is
 # a lot more code though.