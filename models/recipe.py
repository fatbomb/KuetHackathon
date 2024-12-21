from .db import db


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    taste = db.Column(db.String(100), nullable=False)
    cuisine_type = db.Column(db.String(100), nullable=False)
    preparation_time = db.Column(db.Integer, nullable=False)
    reviews = db.Column(db.Float, nullable=True)
    instructions = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
