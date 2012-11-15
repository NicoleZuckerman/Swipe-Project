from math import pow

def get_data_back(path_for_file):
    f = open(path_for_file)
    read = f.read()
    returned_to_dict_form = eval(read)
    return returned_to_dict_form

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
        smoothed_x = (current_point['x']  + previous_point['x'] + next_point['x']) / 3
        smoothed_y = (current_point['y']  + previous_point['y'] + next_point['y']) / 3
        timestamp = current_point['timestamp']
        smoothed_points.append(smoothed_point)
        i = i + 1
        smoothed_point = {'x': smoothed_x, 'y': smoothed_y, 'timestamp': timestamp}
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
    #this may not be necessary because  the list is ordered already
    swipe_in_time_order = sorted(swipe_objects, key=lambda x: x['timestamp'])
    ending_point = swipe_in_time_order[-1]
    last_letter = closest_letter(ending_point)
    return last_letter

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

def guess_bigram():
    start = starting_letter()
    end = ending_letter()
    letters = [start, end]
    return letters
    # return bigram, make sure you send it to the browser

def is_it_a_word_velocity_style(bigram):
    pass
    # check dictionary
    # number of velocity=0 points (plus start and end) indicates minimum number of letters



 # create a class for swipe as well as having one 
 # for datapoint for all the things one can do with a point


 # figure out which keys fall within a certain
 # margin of error of the value- if you find one that's relatively close, you
 # don't need to check the keys all the way across the board.  That way is
 # a lot more code though.