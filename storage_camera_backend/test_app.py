import time
import unittest

from app import app as app, StorageCamera


class TestCameraStorage(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.camera = StorageCamera()

    def test_door_unlocking_with_correct_password(self):
        response = self.client.post('/unlock', json={'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Door is unlocked')
        self.assertEqual(self.camera.state, 'locked')
        self.camera.close_door()

    def test_door_unlocking_with_incorrect_password(self):
        response = self.client.post('/unlock', json={'password': 'incorrect_password'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Error: Door is already unlocked')
        self.camera.close_door()

    def test_door_locking(self):
        response = self.client.post('/unlock', json={'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Door is unlocked')
        response = self.client.post('/lock')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Door is locked')
        self.assertEqual(self.camera.state, 'locked')
        self.camera.close_door()

    def test_get_door_state(self):
        response = self.client.get('/state')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['state'], 'unlocked')
        self.camera.close_door()

    def test_warning_door_not_closed(self):
        response = self.client.post('/unlock', json={'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Error: Door is already unlocked')
        time.sleep(6)
        self.assertFalse(self.camera.is_door_unlocked())
        self.camera.close_door()


if __name__ == '__main__':
    unittest.main()
