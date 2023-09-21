# from app import db
import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app , database_path = database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class FoodItems(db.Model):
  __tablename__ = 'food_items'
  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(200), nullable=False)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def __repr__(self):
    return f"<FoodItems id={self.id}, type={self.type}>"

class TheFood(db.Model):
  __tablename__ = 'the_food'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), nullable=False)
  rate_it = db.Column(db.Integer, db.ForeignKey('food_items.id'))
  food_item = db.relationship('FoodItems', backref='the_food', lazy=True)


  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def __repr__(self):
    return f"<TheFood id={self.id}, name={self.name}>"