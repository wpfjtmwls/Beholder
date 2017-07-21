from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    owner = db.Column(db.String(128))

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def __repr__(self):
        return "<Video n:%s o:%s>" % (self.name, self.owner)

