import json
from hashlib import sha256
from typing import List

from Crypto.Hash import SHA

from pycoin import Transaction

class Block:
    def __init__(self, index: int, transaction: List[str], timestamp: str, previous_hash: str):
        self.index: int = index
        self.transaction: List[str] = transaction
        self.timestamp: str = timestamp
        self.previous_hash: str = previous_hash
        self.hash: str = "0"
        self.merkle_root: str = ""
        self.nonce: int = 0

    def to_dict(self) -> dict:
        self.merkle_root = self.compute_merkle_root()
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'nonce': self.nonce
        }
    
    def to_json(self) -> str:
        self.merkle_root = self.compute_merkle_root()
        return json.dumps(self.__dict__, sort_keys=False)

    def compute_hash(self) -> str:
        self.merkle_root = self.compute_merkle_root()
        payload = str(self.to_dict()).encode()
        return sha256(payload).hexdigest()

    def compute_merkle_root(self) -> str:
        transactionHashes = self.transactionHashes(self.transaction)
        root = self.merkleRoot(transactionHashes)
        return root

    def hash_sum(self, a, b):
        a = str(a).encode()
        b = str(b).encode()
        result = sha256(a + b).hexdigest()
        return result

    def transactionHashes(self, transactions: List[str]):
        return [sha256(str(transaction).encode()).hexdigest() for transaction in transactions]

    def merkleRoot(self, leaves: List[str]):
        if len(leaves) <= 1:
            return leaves[0]

        roots = []
        index = 0
        while index < len(leaves):
            a = leaves[index]
            b = leaves[index+1] if index+1 < len(leaves) else leaves[index]
            root = self.hash_sum(a, b)
            roots.append(root)
            index += 2
        
        return self.merkleRoot(roots)
