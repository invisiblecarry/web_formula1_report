import unittest
import os
from web_report_formula1 import app
from bs4 import BeautifulSoup


class TestFormula1App(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['DATA_FOLDER'] = os.path.join('..', 'data')
        self.app = app.test_client()

    def test_show_report(self):
        response = self.app.get('/report/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        h1_text = soup.find('h1').text
        self.assertEqual(h1_text, 'Common Statistics')
        table = soup.find('table')
        self.assertIsNotNone(table)
        rows = table.find_all('tr')
        self.assertTrue(len(rows) > 1)

    def test_show_driver_list(self):
        response = self.app.get('/report/drivers/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        h1_text = soup.find('h1').text
        self.assertEqual(h1_text, 'Driver List')
        ul = soup.find('ul')
        self.assertIsNotNone(ul)
        items = ul.find_all('li')
        self.assertTrue(len(items) > 0)

    def test_show_driver_info(self):
        response = self.app.get('/report/drivers/info/?driver_id=SVF')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        h1_text = soup.find('h1').text
        self.assertEqual(h1_text, 'Driver Info')

        table = soup.find('table')
        self.assertIsNotNone(table)
        rows = table.find_all('tr')
        self.assertTrue(len(rows) > 1)


if __name__ == '__main__':
    unittest.main()
