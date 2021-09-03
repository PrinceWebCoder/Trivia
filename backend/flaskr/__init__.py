import os
from flask import (Flask,
                  request,
                  abort,
                  jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import (setup_db,
                    Question,
                    Category)

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selections):
  
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE 
  questions = [question.format() for question in selections]
  current_questions = questions[start:end]
  
  return current_questions




# main creation:
def create_app(test_config=None):
 
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={"/": {"origins": "*"}})
  
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  
  @app.route('/categories')
  def get_categories():
    data = Category.query.all()
    categories = {}
    for category in data:
      categories[category.id] = category.type
    
    if len(data) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': categories
    })

  # questions:
  @app.route('/questions')
  def get_questions():
    selection = Question.query.all()
    total_questions = len(selection)
    # this pagination:
    now_questions = paginate_questions(request, selection)
    
    categories = Category.query.all()
    categories_tdd = {}
    for category in categories:
        categories_tdd[category.id] = category.type
    
    if (len(now_questions) == 0):
        abort(404)
    
    
    return jsonify({
        'success': True,
        'questions': now_questions,
        'total_questions': total_questions,
        'categories': categories_tdd
    })

  @app.route('/questions/<int:q_id>', methods=['DELETE'])
  def delete_question(q_id):
    
    question = Question.query.get(q_id)
    
    try:
      question = Question.query.get(q_id)

      if question is None:
        abort(404)
      question.delete()
      
      return jsonify({
        'success': True,
        'deleted': q_id
      })
    except:
      abort(422)
  
  @app.route('/questions',methods=['POST'])
  def create_question():

    data = request.get_json()

    new_question = data['question']
    in_answer = data['answer']
    in_category = data['category']
    in_difficulty = data['difficulty']

    if (len(new_question)==0) or (len(in_answer)==0):
      abort(422)

    question=Question(
      question=new_question,
      answer=in_answer,
      category=in_category,
      difficulty=in_difficulty
    )

    question.insert()
  
    all_questions = Question.query.all()
    current_questions = paginate_questions(request, all_questions)
    lenq = len(all_questions)
    return jsonify({
      'success': True,
      'created': question.id,
      'questions': current_questions,
      'total_questions': lenq
    })
  
  @app.route('/questions/search', methods=['GET','POST'])
  def search_questions():
    
    data = request.get_json()

    if(data['searchTerm']):
      searched_term = data['searchTerm']
    
    
    related_questions = Question.query.filter(Question.question.ilike('%{}%'.format(searched_term))).all()
    
    if related_questions==[]:
      abort(404)
    
    qsp = paginate_questions(request, related_questions)
    
    return jsonify({
      'success': True,
      'questions': qsp,
      'total_questions': len(related_questions)
    })
  
  @app.route('/categories/<int:id>/questions',methods=['GET'])
  def get_questions_by_category(id):
    category = Category.query.get(id)
    if (category is None):
      abort(404)
    
    try:
      questions = Question.query.filter_by(category=category.id).all()
      
      current_questions = paginate_questions(request, questions)
      
      return jsonify({
        'success': True,
        'questions': current_questions,
        'current_category': category.type,
        'total_questions': len(questions)
      })
    except:
      abort(500)
  
  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():
    
    data = request.get_json()

    category = data['quiz_category']
    previous_questions = data['previous_questions']
    
    #####>>>>>
    
    if category['id'] != 0:
      questions = Question.query.filter_by(category=category['id']).all()
    else:
      questions = Question.query.all()

    def get_random_question():
      next_question = random.choice(questions).format()
      return next_question

    next_question = get_random_question()

    used = False
    
    if next_question['id'] in previous_questions:
      used = True
    
    while used:
      next_question = random.choice(questions).format()
    
      if (len(previous_questions) == len(questions)):
        return jsonify({
          'success': True,
          'message': "game over"
          }), 200

    return jsonify({
    'success': True,
    'question': next_question
    })
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    })
    
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422, 
      'message': 'Unprocessable. Syntax error.'
    }), 422
    
  @app.errorhandler(500)
  def internal_server(error):
    return jsonify({
      'success': False,
      'error': 500, 
      'message': 'Sorry, the falut is us not you. Please try again later.'
    }), 500
  
  
  return app




# end of the code...