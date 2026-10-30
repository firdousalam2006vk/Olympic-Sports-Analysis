"""
Olympic-Flask/test_app.py
Unit test suite verifying all routes and REST API endpoints in the Flask application.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app

class TestOlympicFlask(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_01_index_route(self):
        """Test home route / returns HTTP 200 OK."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Global Olympic Sports Performance Analysis", response.data)
        self.assertIn(b"2,823", response.data)

    def test_02_leaderboard_route(self):
        """Test leaderboard route returns HTTP 200 OK with records."""
        response = self.client.get("/leaderboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Olympic National Leaderboard", response.data)
        self.assertIn(b"USA", response.data)

    def test_03_host_advantage_route(self):
        """Test host advantage route returns HTTP 200 OK."""
        response = self.client.get("/host-advantage")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Host Nation Advantage", response.data)
        self.assertIn(b"86.7%", response.data)

    def test_04_funding_roi_route(self):
        """Test funding ROI route returns HTTP 200 OK."""
        response = self.client.get("/funding-roi")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"High-Performance Funding ROI", response.data)
        self.assertIn(b"0.752", response.data)

    def test_05_dashboards_route(self):
        """Test dashboards route returns HTTP 200 OK."""
        response = self.client.get("/dashboards")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Interactive Tableau Public Dashboards", response.data)

    def test_06_api_kpis(self):
        """Test REST API /api/kpis returns valid JSON with 51 editions and 18,905 medals."""
        response = self.client.get("/api/kpis")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["total_editions"], 51)
        self.assertEqual(json_data["total_medals"], 18905)
        self.assertEqual(json_data["total_gold"], 6195)

    def test_07_api_medals(self):
        """Test REST API /api/medals returns country records."""
        response = self.client.get("/api/medals?country=USA")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertGreater(len(json_data), 0)
        self.assertEqual(json_data[0]["noc"], "USA")

    def test_08_api_host_surge(self):
        """Test REST API /api/host-surge returns host records."""
        response = self.client.get("/api/host-surge")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertGreater(len(json_data), 0)

if __name__ == "__main__":
    unittest.main()
