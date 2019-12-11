import datetime
import json
from urllib.parse import urlparse
from hashlib import sha256
from typing import List, Union

import requests
from pyprnt import prnt

from pycoin import Wallet
from pycoin import Transaction
from pycoin import Block

class Blockchain:
    # TODO: Able to change difficulty when the hash power of the network change
    # difficulty should be defined in the Block class instead to complete the above task
    difficulty = 2
    nodes = set()

    def __init__(self, wallet: Wallet):
        self.unconfirmed_transactions: List[str] = []
        self.chain: List[str] = []
        self.create_genesis_block(wallet)

    def create_genesis_block(self, wallet: Wallet):
        block_reward = Transaction("Block_Reward", wallet.pubkey, "5.0").to_json()
        genesis_block = Block(0, [block_reward], datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "0")
        genesis_block.hash = self.proof_of_work(genesis_block)
        self.chain.append(genesis_block.to_json())

    @property
    def last_block(self):
        return json.loads(self.chain[-1])
    
    def register_node(self, node_url):
        # Checking node_url has valid format
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            # Accepts an URL scheme with http in front
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL scheme like '192.168.0.5:5000'
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    # Experimental
    def check_balance(self, address: str) -> float:
        if len(self.chain) <= 0:
            return None

        balance = 0.0

        for block in self.chain:
            block = json.loads(block)
            transactions = block["transaction"]
            for transaction in transactions:
                transaction = json.loads(transaction)
                if transaction["recipient"] == address:
                    balance += float(transaction["value"])
                elif transaction["sender"] == address:
                    balance -= float(transaction["value"])
        for transaction in self.unconfirmed_transactions:
            transaction = json.loads(transaction)
            if transaction["recipient"] == address:
                    balance += float(transaction["value"])
            elif transaction["sender"] == address:
                balance -= float(transaction["value"])
        return balance

    # TODO: Able to charge transaction fee from the sender of the transaction
    def add_new_transaction(self, transaction: Transaction) -> bool:
        if transaction.verify_transaction_signature():
            # Check balance before confirming a transaction
            if transaction.sender != "Block_Reward" and self.check_balance(transaction.sender) >= float(transaction.value):
                self.unconfirmed_transactions.append(transaction.to_json())
                return True
        return False

    def proof_of_work(self, block: Block) -> str:
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def is_valid_proof(self, block: Block, block_hash: str) -> bool:
        return (block_hash.startswith('0' * Blockchain.difficulty) and (block_hash == block.compute_hash()))
    
    def add_block(self, block: Block, proof: str) -> bool:
        previous_hash = self.last_block['hash']
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block.to_json())
        return True

    def mine(self, wallet: Wallet) -> Union[Block, bool]:
        block_reward = Transaction("Block_Reward", wallet.pubkey, "5.0")
        self.unconfirmed_transactions.insert(0, block_reward.to_json())
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

    def valid_chain(self, chain: List[str]) -> bool:
        # Check if a blockchain is valid
        # = Check if all blocks are valid
        current_index = 0
        chain = json.loads(chain)

        while current_index < len(chain):
            block = json.loads(chain[current_index])
            current_block = Block(
                block['index'],
                block['transaction'],
                block['timestamp'],
                block['previous_hash'])
            current_block.merkle_root = block['merkle_root']
            current_block.nonce = block['nonce']

            if current_index + 1 < len(chain):
                if current_block.compute_hash() != json.loads(chain[current_index+1])['previous_hash']:
                    return False
            if isinstance(current_block.transaction, list):
                for transaction in current_block.transaction:
                    transaction = json.loads(transaction)
                    # Skip block reward because it does not have signature
                    if transaction['sender'] == 'Block_Reward':
                        continue
                    current_transaction = Transaction(
                        transaction['sender'],
                        transaction['recipient'],
                        transaction['value'])
                    current_transaction.signature = transaction['signature']
                    # Validate digital signature of each transaction
                    if not current_transaction.verify_transaction_signature():
                        return False
                if not self.is_valid_proof(current_block, block['hash']):
                    return False
            current_index += 1
        return True

    def consensus(self) -> bool:
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

    def hash_sum(self, a, b):
        a = str(a).encode()
        b = str(b).encode()
        result = sha256(a + b).hexdigest()
        return result

    def merkle_path(self, transaction):
        path = []
        transactionHash = sha256(str(transaction.to_json()).encode()).hexdigest()
        block = self.search_block_with_transaction(transactionHash)
        leaves = []
        if block:
            for trans in block['transaction']:
                trans = json.loads(trans)
                new_trans = Transaction(trans['sender'], trans['recipient'], trans['value'])
                if 'signature' in trans.keys():
                    new_trans.signature = trans['signature']
                new_transHash = sha256(str(new_trans.to_json()).encode()).hexdigest()
                leaves.append(new_transHash)
            path = self._merklePath(leaves, transactionHash, [])
            path.append(block['merkle_root'])
        return path

    def search_block_with_transaction(self, transactionHash):
        fullchain = [json.loads(block) for block in self.chain]
        for block in fullchain[::-1]:
            for trans in block['transaction']:
                trans = json.loads(trans)
                new_trans = Transaction(trans['sender'], trans['recipient'], trans['value'])
                if 'signature' in trans.keys():
                    new_trans.signature = trans['signature']
                new_transHash = sha256(str(new_trans.to_json()).encode()).hexdigest()
                
                if transactionHash == new_transHash:
                    return block
        return False

    def _merklePath(self, leaves, point, path):
        if len(leaves) <= 1:
            return path

        roots = []
        next_point = ""
        index = 0
        while index < len(leaves):
            a = leaves[index]
            b = leaves[index+1] if index+1 < len(leaves) else leaves[index]
            root = self.hash_sum(a, b)
            roots.append(root)

            if a == point:
                path.append(["1", b])
                next_point = root
            elif b == point:
                path.append(["0", a])
                next_point = root
            index += 2

        return self._merklePath(roots, next_point, path)

    def partialValidation(self, path, target):
        result = target
        for p in path:
            direction = int(p[0])
            h = p[1]

            if direction == 0:
                result = self.hash_sum(h, result)
            else:
                result = self.hash_sum(result, h)
        return result
