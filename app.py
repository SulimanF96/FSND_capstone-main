  
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import requires_auth, AuthError

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.route('/movies')
  @requires_auth("get:movies")
  def get_movies(payload):
    try:
      movies = [movie.format() for movie in Movie.query.all()]
      return jsonify({
        "success": True,
        "movies": movies
    })
    except:
        abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth("post:movie")
  def create_movie(payload):
     try:
         new_movie = request.get_json()
         movie = Movie(new_movie['title'], new_movie['release_date'] )
         movie.insert()
         return jsonify({
        'success': True,
        'movie': [movie.format() for movie in Movie.query.all()]
      })
     except:
         abort(422)

  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth("patch:movie")
  def update_movie(payload, movie_id):
     updated_movie = request.get_json()
     movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
     if movie is None:
           abort(404)
  
     movie.update(updated_movie)
     
     return jsonify({
        'success': True,
        'movie': [movie.format() for movie in Movie.query.all()]
      })

  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth("delete:movie")
  def delete_movie(payload, movie_id):
     movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
     if movie is None:
           abort(404)
     movie.delete()
     return jsonify({
        'success': True,
        'delete': movie_id
      })
     
  @app.route('/actors')
  @requires_auth("get:actors")
  def get_actors(payload):
    try:
      actors = [actor.format() for actor in Actor.query.all()]
      return jsonify({
        "success": True,
        "actors": actors
    })
    except:
        abort(422)

  @app.route('/actors', methods=['POST'])
  @requires_auth("post:actor")
  def create_actor(payload):
     try:
         new_actor = request.get_json()
         actor = Actor(new_actor['name'], new_actor['age'], new_actor['gender'])
         actor.insert()
         return jsonify({
        'success': True,
        'actors': [actor.format() for actor in Actor.query.all()]
      })
     except:
         abort(422)

  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth("patch:actor")
  def update_actor(payload, actor_id):
     
     updated_actor = request.get_json()
     actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
     
     if actor is None:
           abort(404)
           
     actor.update(updated_actor)
     
     return jsonify({
        'success': True,
        'actors': [actor.format() for actor in Actor.query.all()]
      })

  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth("delete:actor")
  def delete_actor(payload, actor_id):
     actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
     if actor is None:
           abort(404)
     actor.delete()
     return jsonify({
        'success': True,
        'delete': actor_id
      })
     
  ## Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
      }), 400
      
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
      }), 404
      
  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable entity'
      }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
      }), 500
  
  @app.errorhandler(AuthError)
  def authError(AuthError):
    return jsonify({
                    "success": False, 
                    "error": AuthError.status_code,
                    "message": AuthError.error
                    }), AuthError.status_code

  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)