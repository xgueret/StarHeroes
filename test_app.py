import unittest
from app import app

class CalendarTestCase(unittest.TestCase):
    def setUp(self):
        """Configure the app for testing."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        """Test if the home page loads correctly and displays the days of the week and children."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Calendrier Hebdomadaire', response.data)
        self.assertIn(b'Lundi', response.data)
        self.assertIn(b'Mardi', response.data)
        self.assertIn(b'Mercredi', response.data)
        self.assertIn(b'Jeudi', response.data)
        self.assertIn(b'Vendredi', response.data)
        self.assertIn(b'child1', response.data)
        self.assertIn(b'child2', response.data)
        self.assertIn(b'child3', response.data)

    def test_calendar_structure(self):
        """Test if the calendar table structure is correct."""
        response = self.app.get('/')
        self.assertIn(b'<td>child1</td>', response.data)
        self.assertIn(b'<td>child2</td>', response.data)
        self.assertIn(b'<td>child3</td>', response.data)

if __name__ == '__main__':
    unittest.main()
