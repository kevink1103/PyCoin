import unittest
import datetime

from pyprnt import prnt

from pycoin import Wallet
from pycoin import Transaction
from pycoin import Block
from pycoin import Blockchain

class TestWallet(unittest.TestCase):

    def test_wallet_initialize(self):
        wallet = Wallet()

        self.assertIsInstance(wallet, Wallet)

    def test_wallet_sign_transaction(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        signature = wallet.sign_transaction(transaction)

        self.assertIsInstance(signature, str)
        self.assertGreater(len(signature), 0)

    def test_wallet_pubkey(self):
        wallet = Wallet()
        pubkey = wallet.pubkey

        self.assertIsInstance(pubkey, str)
        self.assertGreater(len(pubkey), 0)
    
    def test_wallet_pubkey(self):
        wallet = Wallet()
        secret = wallet.secret

        self.assertIsInstance(secret, str)
        self.assertGreater(len(secret), 0)

class TestTransaction(unittest.TestCase):

    def test_transaction_initialize(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)

        self.assertIsInstance(transaction, Transaction)
    
    def test_transaction_to_dict(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        content = transaction.to_dict()

        self.assertIsInstance(content, dict)
        self.assertEqual(list(content.keys()), ["sender", "recipient", "value"])
    
    def test_transaction_to_json(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        content = transaction.to_json()

        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_transaction_add_signature(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)

        self.assertEqual(hasattr(transaction, "signature"), True)
    
    def test_transaction_verify_transaction_signature(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertEqual(verify, True)
    
    def test_transaction_verify_transaction_signature_wrong_transaction(self):
        wallet1 = Wallet()
        wallet2 = Wallet()
        transaction = Transaction(wallet2.pubkey, "CityU", 50)
        signature = wallet1.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertEqual(verify, False)

    def test_transaction_verify_transaction_signature_wrong_wallet(self):
        wallet1 = Wallet()
        wallet2 = Wallet()
        transaction = Transaction(wallet1.pubkey, "CityU", 50)
        signature = wallet2.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertEqual(verify, False)

class TestBlock(unittest.TestCase):

    def test_block_initialize(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")

        self.assertIsInstance(block, Block)

    def test_block_to_dict(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        content = block.to_dict()

        self.assertIsInstance(content, dict)
        self.assertEqual(list(content.keys()), ["index", "transaction", "timestamp", "previous_hash", "nonce"])

    def test_block_to_json(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        content = block.to_json()

        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_block_compute_hash(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 50)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        hash_val = block.compute_hash()

        self.assertIsInstance(hash_val, str)
        self.assertGreater(len(hash_val), 0)

class TestBlockchain(unittest.TestCase):

    def test_blockchain_initialize_create_genesis_block(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        
        self.assertIsInstance(blockchain, Blockchain)
        self.assertEqual(len(blockchain.chain), 1)

        # transaction = Transaction(wallet.pubkey, "CityU", 50)
        # signature = wallet.sign_transaction(transaction)
        # transaction.add_signature(signature)

if __name__ == "__main__":
    unittest.main()
