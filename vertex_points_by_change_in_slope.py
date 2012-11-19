# I probably won't use this way of getting vertex points at all.  But if I do... here it is.

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