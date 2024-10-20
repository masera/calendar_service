import unittest
from src.app import app

class CalendarServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_event(self):
        response = self.app.post('/events', json={
            "description": "Test Event",
            "time": "2024-01-01T12:00:00"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_event(self):
        response = self.app.post('/events', json={
            "description": "Test Event",
            "time": "2024-01-01T12:00:00"
        })
        event_id = response.json['id']
        response = self.app.get(f'/events/{event_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
