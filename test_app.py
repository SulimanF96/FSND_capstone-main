import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie, Actor, db_drop_and_create_all


casting_assistance_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDgxMmEzYWIyZTQwMDZlZmQyZTA3IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgyMzg5MDYsImV4cCI6MTYwODMyNTMwNiwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.DmXZTUMv8keMSfNf43pWhWY1UFrU_jlXN0vT76C4ch42aHBzt_CwykOA6XcmJXst7IHuRSkY2KeHtsGzNXirZsLL5ov_BXU5sznWtJG5UnJvALHf4XLYTdIACcL6WsZJVmoTp704XhIhW3SNLdpCzjEbWA_LBIMFS_EuIPrAS0ACeYhknvx0arer1DWDZ02rgOD2j_89YImszzvNtSaLf-DuYEoKWzoUl1joAeAKlRUnkQYA5bbc1Q3PLFAHVD2Ea3bRdMaD3un2ndHPIGXUS2tkKJG_m9DQghpPtpFBiwzquoWrrLbUIBYNqFel9OAEYgjJtxagMwUy9CWZX67o_A"
casting_director_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhZDdiMzJjZjMwNDUwMDc2YzIyZTU4IiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgyMzg3NDUsImV4cCI6MTYwODMyNTE0NSwiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.WFnkn4_tmdAr9LC1pFD1pBghwddUn55BQBIOvf1Pa5aRGVLPnmAAsI3SQQhf3H-zujbCd830WnDgYTV2Hl_r10-vLxVAyx4qUY7W88jOKYXa9HQisOGnTjKxhx0gzpFPX8JslsI9ofbczDeLqu9QjjA6jLXq6H1gboNydenWlncLhyju17WEbz90vkawrd_rOTtL4MQ1nssEZZhMLZhNWHjM0jeEDzH0-lN9nL578Ec2YBrjkXuGP824oTKe1Dypb89mJaNlsKNDG87c2l4Spszm3bFYeL6RMoiAtCKZQh1Ps0aoMALUTqMUitn2xh61rppxDt_4dDjHy_2ADFlZZw"
executive_producer= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldRcjd4dks4eU82eWgwZlFUMlFJRSJ9.eyJpc3MiOiJodHRwczovL2Rldi03M2Rpb3Zlby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5OWJiMDU3NWIyZjYwMDY5YWJmZmFlIiwiYXVkIjoiY2Fwc3RvbmVBcGkiLCJpYXQiOjE2MDgyMzg5OTcsImV4cCI6MTYwODMyNTM5NywiYXpwIjoiQUFmb2tFNHIyYWNxUzROSzk0M2l6NExzN0N3amhoWjAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.lUAtEwsqSY9TERG5mYQP-L0qfls2I_F_uBddXz7eMaxO3gBuRreDUY3trLUIoPrIgO09usNhf7voiVPZyA0nPz9KHnxpm8G7BKSZ6fhMUY9rV4qOODyOTMpB3c2CFZWMH80FVxUS5Qf0nLMkpGJYACWYRfv7M7kl6Rb71vqBrwOZKkwJDjTKi8XJoYZebT7nrUj3ahU5p2bkyvYlb9GlQw-5BuNt0Rj5TCA97cRkPWO3B2dt8n9gJRnUU0OPtNlSxqPyNV1ThMDialWU0ko2dvpSXrDDxpIx9Tj8P6w6D8YWzq4BNg2th8bcCbnax-1ltaa3r8FAVmSkkNJ_kOTlAg"

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