from flask import Flask, request, render_template, flash, redirect, url_for, request
import json
import os
import create_keyboard_qtpqaz
import get_letter_chosen
import spell_checker

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def index():
    keyboard = json.dumps(create_keyboard_qtpqaz.keyboard_map())
    # return render_template("html_for_touch.html", keyboard=keyboard)
    return render_template("touch_blog.html", keyboard=keyboard)

@app.route("/your_swipe", methods=["POST"])
def results_of_swipe():
    json_string_data = request.form['data']
    print json_string_data
    swipe_data_objects = json.loads(json_string_data)
    f = open('seed_data/swipe_objects.txt', 'w')
    string_objects = str(swipe_data_objects)
    f.write(string_objects)
    f.close()
    pre_spell_check = get_letter_chosen.put_word_together()
    suggested_word = spell_checker.suggested_correction(pre_spell_check)
    if suggested_word == 'Unknown':
        word = "We could not interpret your word. Please try again"
    else: 
        h = open('seed_data/words_collected.txt', 'r+')
        existing_words = h.read()
        h.write(" " + suggested_word)
        word = existing_words + " " + suggested_word
        h.close

    # smoothed_curve = get_letter_chosen.curve_smoothing()
    stuff_to_give_to_javascript = json.dumps([word, swipe_data_objects]) 

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