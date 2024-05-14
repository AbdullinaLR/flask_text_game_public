from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    agility = db.Column(db.Integer, nullable=False)
