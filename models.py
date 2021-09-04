import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


# database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
DB_USER = os.getenv('DB_USER', 'prince')  
DB_PASSWORD = os.getenv('DB_PASSWORD', '00116600')  
DB_NAME = os.getenv('DB_NAME', 'trivia')  
database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


# database_path = 'postgresql://pzfnndtsregwag:654f9aa0dead87e35ebaa7d157fc05bf510a156ac40ba7ad0cf0884dc1979bad@ec2-54-224-194-214.compute-1.amazonaws.com:5432/devktre3eacrp6'

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    category = Category(type="Sport")
    category.insert()
    category = Category(type="Communication")
    category.insert()
    category = Category(type="Technology")
    category.insert()
    category = Category(type="Other")
    category.insert()
    category = Category(type="Math")
    category.insert()
    question = Question(
        question = "What is website's name?",
        answer = "Trivia",
        category = "Other",
        difficulty = 3 )
    question.insert()
    question = Question(
        question = "5 + 6 * 3 - (8+2) + (5/4/4*8)",
        answer = "23",
        category = "Math",
        difficulty = 4 )
    question.insert()
    question = Question(
        question = "What is very famous kind of sport?",
        answer = "Football",
        category = "Sport",
        difficulty = 5 )
    question.insert()



'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)
  
  
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  def __init__(self, type):
    self.type = type
  
  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }
  