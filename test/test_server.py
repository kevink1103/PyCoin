import unittest

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from pycoin import Wallet
from pycoin import Transaction
from pycoin import Block
from pycoin import Blockchain
from Server import app

class TestWallet(unittest.TestCase):

    def test_wallet_initialize(self):
        wallet = Wallet()

        self.assertIsInstance(wallet, Wallet)

if __name__ == "__main__":
    unittest.main()
