from flask import Flask, render_template, request
import flask.ext.sqlalchemy
from config import DevelopmentConfig
import numpy as np
from common.DTW import DynamicTimeWarping

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask.ext.sqlalchemy.SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)

    def __init__(self, name, birth_date):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Gesture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    raw_data = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    owner = db.relationship('Person', backref=db.backref('gestures',
                                                         lazy='dynamic'))

    def __init__(self, name, raw_data):
        self.name = name
        self.raw_data = raw_data

    def __repr__(self):
        return '<id {}>'.format(self.id)


def convert_gesture_raw_to_np(raw_data):
    raw_data = raw_data.replace('\r', "")
    samples = [sample.split(', ') for sample in raw_data.split('\n')]

    return np.array(samples, dtype=float).reshape(-1, 1)


@app.route('/post_template_gesture', methods=['POST'])
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
            raw_data = r
            # save the results
            results = sorted(
                raw_data
            )
            try:
                result = Gesture(
                    name="Temp",
                    raw_data=raw_data
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")
    return render_template('index.html', errors=errors, results=results)


@app.route('/post_test_gesture', methods=['POST'])
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
            gestures = Gesture.query.all()
            results = []
            for gesture in gestures:
                template = convert_gesture_raw_to_np(gesture.raw_data)
                dist = predictor.calculate_error(template=template, test_data=test)
                results.append({'name' : gesture.name, 'dist' : dist})

    return render_template('prediction_result.html', errors=errors, predictions=results)


if __name__ == '__main__':
    # Create the database tables.
    db.create_all()
    # start the flask loop
    app.run()