  
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  @app.route('/movies')
  def get_movies():
    try:
      movies = [movie.format() for movie in Movie.query.all()]
      return jsonify({
        "success": True,
        "movies": movies
    })
    except:
        abort(422)

  @app.route('/movies', methods=['POST'])
  def create_movie():
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
  def update_movie(movie_id):
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
  def delete_movie(movie_id):
     movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
     if movie is None:
           abort(404)
     movie.delete()
     return jsonify({
        'success': True,
        'delete': movie_id
      })
     
  @app.route('/actors')
  def get_actors():
    try:
      actors = [actor.format() for actor in Actor.query.all()]
      return jsonify({
        "success": True,
        "actors": actors
    })
    except:
        abort(422)

  @app.route('/actors', methods=['POST'])
  def create_actor():
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
  def update_actor(actor_id):
     
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
  def delete_actor(actor_id):
     actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
     if actor is None:
           abort(404)
     actor.delete()
     return jsonify({
        'success': True,
        'delete': actor_id
      })


  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)