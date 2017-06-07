from app import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)

    def __init__(self, name, birth_date):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Gesture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    raw_data = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    owner = db.relationship('Person', backref=db.backref('gestures',
                                                         lazy='dynamic'))

    def __init__(self, name, raw_data):
        self.name = name
        self.raw_data = raw_data

    def __repr__(self):
        return '<id {}>'.format(self.id)