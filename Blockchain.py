import datetime
import json
import requests
from urllib.parse import urlparse
from pyprnt import prnt

from Transaction import Transaction
from Block import Block

class Blockchain:
    difficulty = 2
    nodes = set()

    def __init__(self, myWallet):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block(myWallet)

    def create_genesis_block(self, myWallet):
        block_reward = Transaction("Block_Reward", myWallet.pubkey, "5.0").to_json()
        genesis_block = Block(0, [block_reward], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block.to_json())
    
    def register_node(self, node_url):
        # Checking node_url has valid format
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def add_new_transaction(self, transaction: Transaction):
        if transaction.verify_transaction_signature():
            # Check balance before confirming a transaction
            if transaction.sender != "Block_Reward" and self.check_balance(transaction.sender) <= transaction.value:
                return False
            self.unconfirmed_transactions.append(transaction.to_json())
            return True
        else:
            return False
    
    def add_block(self, block, proof):
        previous_hash = self.last_block['hash']
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block.to_json())
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def consensus(self):
        neighbours = self.nodes
        new_chain = None
        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get('http://' + node + '/fullchain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        # Replace our chain if longer chain is found
        if new_chain:
            self.chain = json.loads(new_chain)
            return True
        return False

    def valid_chain(self, chain):
        # check if a blockchain is valid
        current_index = 0
        chain = json.loads(chain)

        while current_index < len(chain):
            block = json.loads(chain[current_index])
            current_block = Block(
                block['index'],
                block['transaction'],
                block['timestamp'],
                block['previous_hash'])
            current_block.nonce = block['nonce']

            if current_index + 1 < len(chain):
                if current_block.compute_hash() != json.loads(chain[current_index+1])['previous_hash']:
                    return False
            if isinstance(current_block.transaction, list):
                for transaction in current_block.transaction:
                    transaction = json.loads(transaction)
                    # skip Block reward because it does not have signature
                    if transaction['sender'] == 'Block_Reward':
                        continue
                    current_transaction = Transaction(
                        transaction['sender'],
                        transaction['recipient'],
                        transaction['value'])
                    current_transaction.signature = transaction['signature']
                    # validate digital signature of each transaction
                    if not current_transaction.verify_transaction_signature():
                        return False
                if not self.is_valid_proof(current_block, block['hash']):
                    return False
            current_index += 1
        return True

    def mine(self, myWallet):
        block_reward = Transaction("Block_Reward", myWallet.pubkey, "5.0").to_json()
        self.unconfirmed_transactions.insert(0, block_reward)
        if not self.unconfirmed_transactions:
            return False
        
        new_block = Block(
            index=self.last_block['index'] + 1,
            transaction=self.unconfirmed_transactions,
            timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            previous_hash=self.last_block['hash'])

        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            self.unconfirmed_transactions = []
            return new_block
        else:
            return False

    def check_balance(self, address):
        if len(self.chain) == 0:
            return None

        balance = 0

        for block in self.chain:
            block = json.loads(block)
            transactions = [json.loads(transaction) for transaction in block["transaction"]]
            prnt(transactions)
            for transaction in transactions:
                if transaction["recipient"] == address:
                    balance += float(transaction["value"])
                elif transaction["sender"] == address:
                    balance -= float(transaction["value"])
        for transaction in self.unconfirmed_transactions:
            if transaction["recipient"] == address:
                    balance += float(transaction["value"])
            elif transaction["sender"] == address:
                balance -= float(transaction["value"])
        return balance

    @property
    def last_block(self):
        return json.loads(self.chain[-1])
