import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, db_drop_and_create_all


casting_assistance_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDgxMmEzYWIyZTQwMDZlZmQyZTA3IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgwNTI1MTEsImV4cCI6MTYwODEzODkxMSwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.s8i-I4FUlnRn5YXSwoEpj-0hyvqN1LmbFoZPA0_hRG8gwH9LAbVE7K92WsWlkH2JJxg4dTbFRBjhwoxWixuJ9A4RDY2vLTgqXCIxPsoQfMyj1pFGGg0ueK5FSanIyMyMAJTXUWgySM9Ts_UzOvMDkYiXtY2izxm2zM9OJWLWsdEUoxNWIIu3OxCMAZb700LsjTQd0W-4DFf4qcLUMloeYg9dCsIfyA6c83Urof94K2a9SIIz4h3fkpgb79B9Q6yau4cClQFxm_A422mOenLIopHzjjLEwtshVyV3cD3wouTxiAMowv1p5ULsu1hGk2CRS67HQy2sHPTS5shaB6v9jQ"
casting_director_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDdiMzJjZjMwNDUwMDc2YzIyZTU4IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgxNDE1NDIsImV4cCI6MTYwODIyNzk0MiwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.mFvzWep3ebjm4CNTxpkCbfIA7eAzdg66YkQ6CpHLd2B_va3pR6EVWDTh71NaKFW1f1jMms-LaM1xZZeEgDFqwVZqQUrppRTX-higRzvMTZ2UOFrW5lacg22jO4E5_KHiohGTcYSnt-fkRxBVlnl-kGICB8uYEAMCGzyP_gqkl--I-cASEgSn9Or6c1TZ9qtOyIyZJgSqdIfAXWWHFMjJ_G13_r1utHqOq7wVLzlh4DQ8iY2M79qI0AjRnL-uy0j4xdOoA-prnZ9RmkMz0HMz3iej4WIx5jlhgCKHl-JJqGkJyZFsKvjGG29QFHUmGeB0eWkFoWhkU3rn_R8cM1DvxA"
executive_producer= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5OWJiMDU3NWIyZjYwMDY5YWJmZmFlIiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgxNDE3NTgsImV4cCI6MTYwODIyODE1OCwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.UOO7HjQ6n-aAmY3EQcfuCXubBJ9ieNbLUAZFfTFGjRLqpbHmBW_ar5T-cAqinEZNHTlo4t4A9mmehlJJ1c9dBVW9o7fOhOcJ4RhtbDV0mgfAyANM3cX7cFPZspXrb_JZ5YIaEO45VgYivLRF6HnxdD83gEs7Ug1h-x3d-Pitue0tOOJkwd_OGlUGs4fouwDrRxfyiNCQfrB6XLuf4P_L7_ygf6NW6Rvbys81njBbxRNuEBo7NQJ7N2_plhaEjXW1NHqkuveYZ62jz15o2qxilCYGBUvdmrsGrdij788FvMmWXsxUhwWGrvVmD0XMopAvgudA-b7smGb7VRPprRusxw"

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
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
        self.assertEqual(data['message']['code'], 'Unauthorized')
        
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
        self.assertEqual(data['message']['code'], 'Unauthorized')
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()