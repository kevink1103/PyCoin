import unittest
import requests
import json
import time

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from Server import app

from pyprnt import prnt

class TestServer(unittest.TestCase):

    def test_server_node1_status(self):
        response = requests.get("http://127.0.0.1:5000/status")
        self.assertEqual(response.status_code, 200)

    def test_server_node2_status(self):
        response = requests.get("http://127.0.0.1:5001/status")
        self.assertEqual(response.status_code, 200)

    def test_server_node3_status(self):
        response = requests.get("http://127.0.0.1:5002/status")
        self.assertEqual(response.status_code, 200)

    def test_server_register_nodes(self):
        response = requests.post("http://127.0.0.1:5001/register_node", data={
            "node": "127.0.0.1:5000"
        })
        self.assertEqual(response.status_code, 201)
        response = requests.post("http://127.0.0.1:5002/register_node", data={
            "node": "127.0.0.1:5001"
        })
        self.assertEqual(response.status_code, 201)

    def test_server_fullchain(self):
        response = requests.get("http://127.0.0.1:5000/fullchain")
        self.assertEqual(response.status_code, 200)
        response = requests.get("http://127.0.0.1:5001/fullchain")
        self.assertEqual(response.status_code, 200)
        response = requests.get("http://127.0.0.1:5002/fullchain")
        self.assertEqual(response.status_code, 200)

    def test_server_mine(self):
        response = requests.get("http://127.0.0.1:5001/mine")
        self.assertEqual(response.status_code, 200)

        response1 = requests.get("http://127.0.0.1:5000/fullchain").json()
        response2 = requests.get("http://127.0.0.1:5001/fullchain").json()
        response3 = requests.get("http://127.0.0.1:5002/fullchain").json()
        self.assertTrue(response1 == response2 and response2 == response3)
    
    def test_server_new_transaction(self):
        response = requests.post("http://127.0.0.1:5001/new_transaction", data={
            "recipient_address": "TEST_TEST",
            "value": "5"
        })
        self.assertEqual(response.status_code, 201)

    def test_server_new_transaction_no_balance(self):
        response = requests.post("http://127.0.0.1:5000/new_transaction", data={
            "recipient_address": "TEST_TEST",
            "value": "500"
        })
        self.assertEqual(response.status_code, 406)

    def test_server_mine_transaction(self):
        response = requests.get("http://127.0.0.1:5001/mine")
        self.assertEqual(response.status_code, 200)

        response1 = requests.get("http://127.0.0.1:5000/fullchain").json()
        response2 = requests.get("http://127.0.0.1:5001/fullchain").json()
        response3 = requests.get("http://127.0.0.1:5002/fullchain").json()
        self.assertTrue(response1 == response2 and response2 == response3)

if __name__ == "__main__":
    unittest.main()
