from flask import Flask, render_template, request
from config import DevelopmentConfig
import numpy as np
from common.DTW import DynamicTimeWarping
from google.appengine.ext import ndb
from flask import jsonify
from flask import Response
import json
from common.Helper import convert_gesture_raw_to_np

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


class Gesture(ndb.Model):
    name = ndb.TextProperty()
    raw_data = ndb.TextProperty()


@app.route('/', methods=['GET'])
def test():
    return "Test"


@app.route('/gesture/template', methods=['POST'])
def post_template_gesture():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        try:
            r = request.get_data()
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('index.html', errors=errors)
        if r:
            try:
                result = Gesture(
                    name="Test",
                    raw_data=r
                )
                result.put()
            except:
                errors.append("Unable to add item to database.")
                return render_template('index.html', errors=errors)
    return jsonify(result.to_dict())


# @app.route('/gesture/fulltest', methods=['POST'])
# def post_full_test_gesture():
#     errors = []
#     results = {}
#     if request.method == "POST":
#         # get url that the person has entered
#         try:
#             r = request.get_data()
#         except:
#             errors.append(
#                 "Unable to get URL. Please make sure it's valid and try again."
#             )
#             return render_template('index.html', errors=errors)
#         if r:
#             test = convert_gesture_raw_to_np(r)
#
#             predictor = DynamicTimeWarping()
#             gestures = Gesture.query().fetch()
#             results = []
#             for gesture in gestures:
#                 template = convert_gesture_raw_to_np(gesture.raw_data)
#                 dist_gyro = predictor.calculate_error_full_dtw(template=template[:, :3], test_data=test[:, :3])
#                 dist_acc = predictor.calculate_error_full_dtw(template=template[:, 3:6], test_data=test[:, 3:6])
#                 dist_mag = predictor.calculate_error_full_dtw(template=template[:, 6:9], test_data=test[:, 6:9])
#                 dist_ori = predictor.calculate_error_full_dtw(template=template[:, 9:12], test_data=test[:, 9:12])
#                 dist_total = predictor.calculate_error_full_dtw(template=template, test_data=test)
#
#                 results.append(json.dumps({"Gesture" : gesture.name,
#                                            "Distance Total" : dist_total,
#                                            "Distance Gyro" : dist_gyro,
#                                            "Distance Accelerometer": dist_acc,
#                                            "Distance Magnetometer" : dist_mag,
#                                            "Distance Orientation" : dist_ori}))
#
#     return Response(json.dumps(results), mimetype='application/json')


@app.route('/gesture/test', methods=['POST'])
def post_test_gesture():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        try:
            r = request.get_data()
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('index.html', errors=errors)
        if r:
            test = convert_gesture_raw_to_np(r)
            predictor = DynamicTimeWarping()
            gestures = Gesture.query().fetch()
            results = []
            for gesture in gestures:
                template = convert_gesture_raw_to_np(gesture.raw_data)
                dist_total = predictor.calculate_error_full_dtw(template=template, test_data=test)
                results.append(json.dumps({"Gesture" : gesture.name,
                                           "Distance Total" : dist_total}))

    return Response(json.dumps(results), mimetype='application/json')


@app.route('/gesture', methods=['GET'])
def return_gesture_templates():
    results = {}
    if request.method == "GET":
        gestures = Gesture.query().fetch()
        results = []
        for gesture in gestures:
            results.append(gesture.to_dict())

    return Response(json.dumps(results), mimetype='application/json')


    # if __name__ == '__main__':
    #     # Create the database tables.
    #     db.create_all()
    #     # start the flask loop
    #     app.run()
