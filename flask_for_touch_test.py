from flask import Flask, request, render_template, flash, redirect, url_for, request
import json
# from flask_heroku import Heroku
import os
from skaffold import Skaffold

app = Flask(__name__)
# heroku = Heroku(app)
app.config.from_object(__name__)
### If you need Skaffold:
# Skaffold(app, class-name, db_session)
# Skaffold(app, class-name, db_session)

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
        points = [ cls(pt['x'], pt['y'], pt['timeStamp']) for pt in data]
        return points

    # __str__ will give the string version of objects.  
    # Since two things could be identical, it would overwrite;
    # __repr__ gives a unique representation of the objects within
    def __repr__(self):
        return "DataPoint(%d, %d, %d)" % (self.x, self.y, self.timeStamp)

# in order to get the data back out of the file:
def get_data_back():
    f = open('seed_data/swipe_objects.txt')
    read = f.readline()
    return_to_dict_form = eval(read)


@app.route("/")
def index():
    return render_template("html_for_touch_test.html")

@app.route("/your_swipe", methods=["POST"])
def results_of_swipe():
    json_string_data = request.form['data']
    print json_string_data
    swipe_data_objects =Datapoint.from_json(json_string_data)
    f = open('seed_data/swipe_objects.txt', 'w')
    # change to mode 'a' if you want to append instead of overwrite
    string_objects = str(swipe_data_objects)
    f.write(string_objects)
    f.close()

    return render_template("test_results.html", swipe_data_object = swipe_data_objects)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")