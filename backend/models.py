from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Recipe {self.title}>"
    """
    the following methods added underneath are convinience methods
    """
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, title, description):
        self.title = title
        self.description = description
        db.session.commit()        


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<Recipe {self.username}>"

    """
    the following methods added underneath are convinience methods
    """
    def save(self):
        db.session.add(self)
        db.session.commit()