import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, db_drop_and_create_all


casting_assistance_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDgxMmEzYWIyZTQwMDZlZmQyZTA3IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgwNTI1MTEsImV4cCI6MTYwODEzODkxMSwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.s8i-I4FUlnRn5YXSwoEpj-0hyvqN1LmbFoZPA0_hRG8gwH9LAbVE7K92WsWlkH2JJxg4dTbFRBjhwoxWixuJ9A4RDY2vLTgqXCIxPsoQfMyj1pFGGg0ueK5FSanIyMyMAJTXUWgySM9Ts_UzOvMDkYiXtY2izxm2zM9OJWLWsdEUoxNWIIu3OxCMAZb700LsjTQd0W-4DFf4qcLUMloeYg9dCsIfyA6c83Urof94K2a9SIIz4h3fkpgb79B9Q6yau4cClQFxm_A422mOenLIopHzjjLEwtshVyV3cD3wouTxiAMowv1p5ULsu1hGk2CRS67HQy2sHPTS5shaB6v9jQ"
casting_director_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDdiMzJjZjMwNDUwMDc2YzIyZTU4IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgwNTI4NzksImV4cCI6MTYwODEzOTI3OSwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.Q7X7551DAfZjjqWoptRo1qcQCpJJhDKg870HxlDfeisg1aZqnGcj78_kAC0bEapJroiVDej2DLz-SO24vji6GNNP-3AmNMYYuEZ3flnAIH5HLc74Sv8i1LngdtZ-EIV-a-6sm0XT8gVKyUJL1sNzVqUY2rZDAZubPx5u1gX0eg1qR37m2Htng2-Kx252QZftRuTRo4-3meDVMzKLS5uYIDj6nSsq_7Det6iY7WdOqW83XmoNu4lUsWhob0Uk8Up6NuFg-qf7aOMfJRKOhP1CPzTrzpCzswxT0vQy_mgzW2VQJPXyjIw6s4aXNkyzqtozTGEGZEapJj-Mlev_46Ol1w"
executive_producer= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5OWJiMDU3NWIyZjYwMDY5YWJmZmFlIiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgwNTMyMjAsImV4cCI6MTYwODEzOTYyMCwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.B6ASZU5EZRXPW6hAYIz6yVK-oB6Ny8jPIj5smpmRp-osZxBmQwR6p2gPdWsK-OKhDs3o3MDCYr2p1Hno92bgWZCEiW7RXNpguUt7qJKsZ1ciJn7mIRMpciK2DdNFmGHTPRp_4OmP9MeCU1_iYtFRvoo8b4y6N6QrdwwdZcjKPF4UnaN_MTeLQd6OOclSlwQdlFBauyyVJt79HcYBJCzzaHQpTPc3dZXGOUeX4xuyAvYSYMrr__voqiAheHsyGvnXSOVEFtu6vmiuWcGhDDiFOoDXouvj95ZI8UgEyMkhlD1teAc9iI_HUZC6e2F_wEwz5zk71NiL_BCsgTOmUy6bPA"

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}/{}".format('postgres:1234Qwer@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
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
        
    # def test_patch_movie(self):
    #     movie = Movie.query.first().format()
    #     res = self.client().delete('/movies/' + str(movie['id']), json={"title": "test"}, headers={'Authorization': 'Bearer ' + executive_producer})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
        
    def test_404_patch_using_unexisting_id(self):
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
        
    # def test_patch_actor(self):
    #     actor = Actor.query.first().format()
    #     res = self.client().delete('/actors/' + str(actor['id']), json={"name": "test"}, headers={'Authorization': 'Bearer ' + executive_producer})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['actors']))
        
    def test_404_patch_using_unexisting_id_for_actor(self):
        res = self.client().delete('/actors/100000', headers={'Authorization': 'Bearer ' + executive_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()