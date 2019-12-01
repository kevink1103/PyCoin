import unittest

from pyprnt import prnt

from pycoin.Wallet import Wallet
from pycoin.Transaction import Transaction

wallet = Wallet()
transaction = Transaction(wallet.pubkey, 'CityU', 50)

class TestWallet(unittest.TestCase):

    def test_wallet_initialize(self):
        self.assertIsInstance(wallet, Wallet)

    def test_wallet_sign_transaction(self):
        signature = wallet.sign_transaction(transaction)
        self.assertIsInstance(signature, str)
        self.assertGreater(len(signature), 0)

    def test_wallet_pubkey(self):
        pubkey = wallet.pubkey
        self.assertIsInstance(pubkey, str)
        self.assertGreater(len(pubkey), 0)
    
    def test_wallet_pubkey(self):
        secret = wallet.secret
        self.assertIsInstance(secret, str)
        self.assertGreater(len(secret), 0)

class TestTransaction(unittest.TestCase):

    def test_transaction_initialize(self):
        self.assertIsInstance(transaction, Transaction)
    
    def test_transaction_to_dict(self):
        content = transaction.to_dict()
        self.assertIsInstance(content, dict)
        self.assertEqual(list(content.keys()), ['sender', 'recipient', 'value'])
    
    def test_transaction_to_json(self):
        content = transaction.to_json()
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_transaction_add_signature(self):
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        self.assertEqual(hasattr(transaction, 'signature'), True)
    
    def test_transaction_verify_transaction_signature(self):
        verify = transaction.verify_transaction_signature()
        self.assertEqual(verify, True)
    
    def test_transaction_verify_transaction_signature_fake(self):
        fake_transaction = Transaction(Wallet().pubkey, 'CityU', 100)
        signature = wallet.sign_transaction(fake_transaction)
        fake_transaction.add_signature(signature)
        verify = fake_transaction.verify_transaction_signature()
        self.assertEqual(verify, False)

if __name__ == "__main__":
    unittest.main()
