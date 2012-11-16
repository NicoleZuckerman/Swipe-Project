from math import pow, cos
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
    data_dicts = get_data_back('seed_data/swipe_objects.txt')
    letters_crossed = []
    for point in data_dicts:
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

def vertex_points_by_change_in_slope():
    smoothed_curve = curve_smoothing()
    points_of_change = []
    # i is 1 because we don't need to check the first point, we know it's an inflection already
    i = 1
    end = len(smoothed_curve) - 1
    point_of_change = {}

    while i < end:
        previous_point = smoothed_curve[i - 1]
        next_point = smoothed_curve[i + 1]
        current_point = smoothed_curve[i]
        # print current_point
        rise1 = float(current_point['y'] - previous_point['y'])
        print "This is current y : %r" % current_point['y']
        print "This is previous y: %r" % previous_point['y']

        print "This is rise 1: %d" % rise1

        rise2 = float(next_point['y'] - current_point['y'])
        print "This is rise 2: %d" % rise2

        run1 = float(current_point['x'] - previous_point['x'])
        print "This is run 1: %d" % run1

        run2 = float(next_point['x'] - current_point['x'])
        print "This is run 2: %d" % run2

        try: 
            slope1 = float(rise1 / run1)
            print "This is slope 1: %d" % slope1
        except ZeroDivisionError:
            slope1 = "undefined"
            print "This is slope 1: %s" % slope1

        try:
            slope2 = float(rise2 / run2)
            print "This is slope 2: %d" % slope2
        except ZeroDivisionError:
            slope1 = "undefined"
            print "This is slope 2: %s" % slope2
        # if slope is undefined, what do I do then?
        # points_of_change.append(current_point)
        # if the difference between the slopes is non-trivial, 
        # record current point in the list of points of change. We'll get that letter later

        i = i + 1
    # points_of_change.append(last_point)
    # error margin- what makes it non-trivial? 15 degrees? 20 degrees?
    # get tangents
# do_it = get_all_vertex_points()


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