import unittest
import datetime

from pyprnt import prnt

try:
    from pycoin import Wallet
    from pycoin import Transaction
    from pycoin import Block
    from pycoin import Blockchain
except:
    import os,sys,inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
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
        transaction = Transaction(wallet.pubkey, "CityU", 1)
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
        transaction = Transaction(wallet.pubkey, "CityU", 1)

        self.assertIsInstance(transaction, Transaction)
    
    def test_transaction_to_dict(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        content = transaction.to_dict()

        self.assertIsInstance(content, dict)
        self.assertEqual(list(content.keys()), ["sender", "recipient", "value"])
    
    def test_transaction_to_json(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        content = transaction.to_json()

        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_transaction_add_signature(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)

        self.assertTrue(hasattr(transaction, "signature"))
    
    def test_transaction_verify_transaction_signature(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertTrue(verify)
    
    def test_transaction_verify_transaction_signature_wrong_transaction(self):
        wallet1 = Wallet()
        wallet2 = Wallet()
        transaction = Transaction(wallet2.pubkey, "CityU", 1)
        signature = wallet1.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertFalse(verify)

    def test_transaction_verify_transaction_signature_wrong_wallet(self):
        wallet1 = Wallet()
        wallet2 = Wallet()
        transaction = Transaction(wallet1.pubkey, "CityU", 1)
        signature = wallet2.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertFalse(verify)

class TestBlock(unittest.TestCase):

    def test_block_initialize(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")

        self.assertIsInstance(block, Block)

    def test_block_to_dict(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        content = block.to_dict()

        self.assertIsInstance(content, dict)
        self.assertEqual(list(content.keys()), ["index", "transaction", "timestamp", "previous_hash", "nonce"])

    def test_block_to_json(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        content = block.to_json()

        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_block_compute_hash(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
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

    def test_blockchain_register_node(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        blockchain.register_node("http://127.0.0.1:101")
        blockchain.register_node("127.0.0.1:102")
        
        self.assertTrue("127.0.0.1:101" in blockchain.nodes)
        self.assertTrue("127.0.0.1:102" in blockchain.nodes)

    def test_blockchain_check_balance(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        balance = blockchain.check_balance(wallet.pubkey)
        
        self.assertGreater(balance, 0)

    def test_blockchain_add_new_transaction_enough_balance(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        blockchain.add_new_transaction(transaction)

        self.assertEqual(len(blockchain.unconfirmed_transactions), 1)

    def test_blockchain_add_new_transaction_not_enough_balance(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 100)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        blockchain.add_new_transaction(transaction)

        self.assertEqual(len(blockchain.unconfirmed_transactions), 0)

if __name__ == "__main__":
    unittest.main()
