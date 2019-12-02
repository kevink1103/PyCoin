import unittest
import datetime

from pyprnt import prnt

import os, sys, inspect
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

    def test_wallet_sign_transaction_valid(self):
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

    def test_transaction_verify_transaction_signature_no_signature(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        verify = transaction.verify_transaction_signature()

        self.assertFalse(verify)
    
    def test_transaction_verify_transaction_signature_wrong_transaction(self):
        wallet = Wallet()
        wrong = Wallet()
        transaction = Transaction(wrong.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertFalse(verify)

    def test_transaction_verify_transaction_signature_wrong_wallet(self):
        wallet = Wallet()
        wrong = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wrong.sign_transaction(transaction)
        transaction.add_signature(signature)
        verify = transaction.verify_transaction_signature()

        self.assertFalse(verify)

    def test_transaction_verify_transaction_signature_too_large_signature(self):
        wallet = Wallet()
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        transaction.add_signature("3379cc2f08e4cde5d24af02611c32693b18f406d4b58fbcd2bbd0acc67b1d")
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

    def test_blockchain_last_block(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        block = blockchain.last_block

        self.assertGreater(len(block), 0)

    def test_blockchain_register_node(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        blockchain.register_node("http://127.0.0.1:101")
        blockchain.register_node("127.0.0.1:102")
        
        self.assertTrue("127.0.0.1:101" in blockchain.nodes)
        self.assertTrue("127.0.0.1:102" in blockchain.nodes)

    def test_blockchain_register_node_wrong_address(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        
        self.assertRaises(ValueError, blockchain.register_node, "")

    def test_blockchain_check_balance(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        balance = blockchain.check_balance(wallet.pubkey)
        
        self.assertGreater(balance, 0)

    def test_blockchain_check_balance_no_chain(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        blockchain.chain = []
        balance = blockchain.check_balance(wallet.pubkey)
        
        self.assertFalse(balance)

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

    def test_blockchain_proof_of_work(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        previous_hash = blockchain.last_block["hash"]
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), previous_hash)
        computed_hash = blockchain.proof_of_work(block)
        
        self.assertGreater(len(computed_hash), 0)

    def test_blockchain_proof_of_work_bad_block(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        previous_hash = blockchain.last_block["hash"]
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), previous_hash)
        delattr(block, "transaction")

        self.assertRaises(AttributeError, blockchain.proof_of_work, block)

    def test_blockchain_is_valid_proof(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        previous_hash = blockchain.last_block["hash"]
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), previous_hash)
        computed_hash = blockchain.proof_of_work(block)
        valid = blockchain.is_valid_proof(block, computed_hash)
        
        self.assertTrue(valid)

    def test_blockchain_add_block(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        previous_hash = blockchain.last_block["hash"]
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), previous_hash)
        computed_hash = blockchain.proof_of_work(block)
        result = blockchain.add_block(block, computed_hash)

        self.assertTrue(result)

    def test_blockchain_add_block_wrong_previous_hash(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "Wrong")
        computed_hash = blockchain.proof_of_work(block)
        result = blockchain.add_block(block, computed_hash)

        self.assertFalse(result)

    def test_blockchain_add_block_wrong_proof(self):
        wallet = Wallet()
        blockchain = Blockchain(wallet)
        transaction = Transaction(wallet.pubkey, "CityU", 1)
        signature = wallet.sign_transaction(transaction)
        transaction.add_signature(signature)
        previous_hash = blockchain.last_block["hash"]
        block = Block(0, [transaction.to_json()], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), previous_hash)
        computed_hash = "Wrong"
        result = blockchain.add_block(block, computed_hash)

        self.assertFalse(result)

    def test_blockchain_mine(self):
        pass

if __name__ == "__main__":
    unittest.main()
