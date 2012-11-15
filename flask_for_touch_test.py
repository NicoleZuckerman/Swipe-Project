from flask import Flask, request, render_template, flash, redirect, url_for, request
import json
# from flask_heroku import Heroku
import os
from skaffold import Skaffold
import create_keyboard_qtpqaz
import get_letter_chosen

app = Flask(__name__)
# heroku = Heroku(app)
app.config.from_object(__name__)
### If you need Skaffold:
# Skaffold(app, class-name, db_session)
# Skaffold(app, class-name, db_session)


@app.route("/")
def index():
    keyboard = create_keyboard_qtpqaz.keyboard_map()
    return render_template("html_for_touch.html", keyboard=keyboard)

# @app.route("/word")
# def word_chosen():
#     f = open('seed_data/swipe_objects.txt', 'w')
#     two_letters = get_letter_chosen.guess_bigram()
#     first_letter = two_letters[0]
#     last_letter = two_letters[-1]
#     keyboard = create_keyboard_qtpqaz.keyboard_map()
#     return render_template("test_results.html", keyboard=keyboard, first_letter=first_letter, last_letter=last_letter,)

@app.route("/your_swipe", methods=["POST"])
def results_of_swipe():
    json_string_data = request.form['data']
    swipe_data_objects = json.loads(json_string_data)
    f = open('seed_data/swipe_objects.txt', 'w')
    # change to mode 'a' if you want to append instead of overwrite
    string_objects = str(swipe_data_objects)
    f.write(string_objects)
    f.close()

    two_letters = get_letter_chosen.guess_bigram()
    first_letter = two_letters[0]
    last_letter = two_letters[-1]
    letters_crossed = get_letter_chosen.letters_path_crosses()
    smoothed_curve = get_letter_chosen.curve_smoothing()
    f.close()

    stuff_to_give_to_javascript = json.dumps([first_letter, last_letter, smoothed_curve, letters_crossed])
    return stuff_to_give_to_javascript

@app.route("/your_calibrations", methods=["POST"])
def results_of_calibration():
    json_string_data = request.form['data']
    un_jsoned_data = json.loads(json_string_data)
    f = open('seed_data/swipe_calibration.txt', 'w')
    # mode 'a' if you want to append, mode 'w' to overwrite
    list_of_letters_and_coordinates = []
    for letter_data in un_jsoned_data:

        calibrated_letter = letter_data[0]
        data = letter_data[1]
        
        points = [(pt['x'], pt['y'], pt['timestamp']) for pt in data]
        letter_and_coordinates = [calibrated_letter, points]
        list_of_letters_and_coordinates.append(letter_and_coordinates)
    string_objects = str(list_of_letters_and_coordinates)
    f.write(string_objects)
    f.close()

    return redirect(url_for("index"))

@app.route("/swipe_calibration")
def calibrate():
    return render_template("touch_calibration.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")