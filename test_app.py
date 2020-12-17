import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie, Actor, db_drop_and_create_all


casting_assistance_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDgxMmEzYWIyZTQwMDZlZmQyZTA3IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgyMjU3MzMsImV4cCI6MTYwODMxMjEzMywiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.KhR4yM4AgzlYvogewTBF5v1N5QF0O3JAswuLFpsczV7zoGn4K6DgsHllC_9wd4TgKza0J7vwSNUUYdetAGnhub3bONtJHKCwoTPXFDnY9OOD1tFnAf62MlZMAXKGBG6IqG40K8SUzjFJ23vZQJF7wrMe0RuCsRLmi-taCn2nH_qgRYirV7IVL7qvq8jNZ3GvG0McghrQ97euvkeK4Rn9aHsYdbqCUrci5_IbSLExTXQq-Q94MxM5slxQXZgAGx9m-BKukyU-ZHA498HofPG81zULkCvNGtJoYeIuA9F-581e8pLwnmm565NfljCMEToswIFn8_fAbHKOcOQGoA-tlg"
casting_director_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDdiMzJjZjMwNDUwMDc2YzIyZTU4IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgyMjU2MzEsImV4cCI6MTYwODMxMjAzMSwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.bwu9IWND3r6ntaTr1v6GypofteR6z7Q8gfTits4VZaLeb8kdOh1kF-PmgX8LG-viCxI-5L2-u-8HAT7xzyrsaL93X1jWOyHrXwdYakKhnRwR6wytsBjDe90vXNl1hPj3fVjoHPsR1iVTHAlJOaJct_LxLnboV2Q3CwtHXIfVchVSytdVa_07Vm-7u4gw2hXm-ZZysWq9vlEKkQXec7V1GI33muc-_o2E_mxRfHLvpo13pE30uuU5J_8cj9VAsgA0QZEMJjdLy1lBOs2vQut1HR_oP0PHRZ4D9LEibaBLQGvkiRWNy6AiLUBGgGLfwWHbiW2-InFAnNIvNUG7r7jm1g"
executive_producer= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5OWJiMDU3NWIyZjYwMDY5YWJmZmFlIiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgyMjU3OTIsImV4cCI6MTYwODMxMjE5MiwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.GN3UxFsN0_WR4iQFSc2ylFzx6CNLI_CHRcnvr3_T3pC1rv0e88IIys0gBB5ukive5-cKngjsd9VVc6q2UuLKYcZAk6ZzVEqHxPMH7udDS1TEKXr62TMl8mFeni0NaEG2SsnX_uWyN6AAjKBqLkZU4u-sNOJhaIQht4RNy4wrgrFkU9WV558NP9ZpWbbpGeWbLyfrk62Y-93DL4Vyh2u9niXW93zHTL7FCDHgCsJkiamsx-_8_fm8PgXh5cbivaXou4eLapBvZRdyWRQkR7viuWc4X53XhnA4vf4-vaLXTCV-eDBl7DXc7RNEKpnNdn_M0t3Jkz91wPOxAuYVx2BTxQ"

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}/{}".format('postgres:1234Qwer@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path, True)
        
        self.new_movie = {
            'title': 'test title',
            'release_date': 'test release_date',
        }

        self.new_actor = {
            'name': 'test name',
            'age': 12,
            'gender': 'test gender'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        # db_drop_and_create_all()
        """Executed after reach test"""
        pass

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie,  headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))
                        
    def test_400_bad_request(self):
        res = self.client().post('/movies', json={"title":"rwe"}, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')
        
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
            
    def test_404_request_wrong_endpoint(self):
        res = self.client().get('/moviess', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        
    # def test_patch_movie(self):
    #     movie = Movie.query.first().format()
    #     res = self.client().patch('/movies/' + str(movie['id']), json={"title": "test"}, headers={'Authorization': 'Bearer ' + executive_producer})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
        
    # def test_404_patch_using_unexisting_id(self):
    #     res = self.client().patch('/movies/100000', headers={'Authorization': 'Bearer ' + executive_producer})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['message'], 'resource not found')
        
    def test_delete_movie(self):
        movie = Movie.query.first().format()
        res = self.client().delete('/movies/' + str(movie['id']), headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], str(movie['id']))
            
    def test_404_delete_using_unexisting_id(self):
        res = self.client().delete('/movies/100000', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

        
    def test_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
                        
    def test_400_bad_request_for_create_actor(self):
        res = self.client().post('/actors', json={"name":"rwe"}, headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')
        
            
    # def test_patch_actor(self):
    #     actor = Actor.query.first().format()
    #     res = self.client().patch('/actors/' + str(actor['id']), json={"name": "test"}, headers={'Authorization': 'Bearer ' + executive_producer})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['actors']))
        
    # def test_404_patch_using_unexisting_id_for_actor(self):
    #     res = self.client().patch('/actors/100000', headers={'Authorization': 'Bearer ' + executive_producer})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['message'], 'resource not found')
        
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
            
    def test_404_request_wrong_endpoint_for_get_actors(self):
        res = self.client().get('/actorss', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_delete_actor(self):
        actor = Actor.query.first().format()
        res = self.client().delete('/actors/' + str(actor['id']), headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], str(actor['id']))
            
    def test_404_delete_using_unexisting_id_for_actor(self):
        res = self.client().delete('/actors/100000', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        
        
    def test_create_movie_using_casting_assistance_token(self):
        res = self.client().post('/movies', json=self.new_movie,  headers={'Authorization': 'Bearer ' + casting_assistance_token})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'Forbidden')
        
    def test_create_movie_using_casting_director_token(self):
        res = self.client().post('/movies', json=self.new_movie,  headers={'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'Forbidden')
        
    def test_create_actor_using_casting_director_token(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer ' + casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        
    def test_create_actor_using_casting_assistance_token(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer ' + casting_assistance_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'Forbidden')
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()