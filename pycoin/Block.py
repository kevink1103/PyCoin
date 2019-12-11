import json
from hashlib import sha256
from typing import List

from Crypto.Hash import SHA

from pycoin import Transaction

# EE4017 Lab 5


class Block:
    """
    a block consists of 6 parameters including
     1. Index,
     2. Transactions,
     3. Timestamp
     4. Hash value of the last block
     5. Hash value of this block
     6. Root of a Merkle tree containing transaction data
     7. Nonce value
     8. Difficulty Level (For changing difficulty when the hash power of the network change)
        [we need to calculate hash value and nonce after adding the transactions.]
    """
    # TODO: Able to change difficulty when the hash power of the network change
    # constructor to create a block
    def __init__(self, index: int, transaction: List[str], timestamp: str, previous_hash: str):
        self.index: int = index
        self.transaction: List[str] = transaction
        self.timestamp: str = timestamp
        self.previous_hash: str = previous_hash
        self.hash: str = "0"
        self.merkle_root: str = ""
        self.nonce: int = 0
        # self.difficulty = 2   # initial difficulty

    # method to dump all contents in the block
    def to_dict(self) -> dict:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'nonce': self.nonce
            # 'difficulty': self.difficulty
        }

    # method to transfer blocks to other peers using json format.
    def to_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=False)

    # method to calculate the hash value of a block
    # we don’t need the empty hash value as the input for the hash function,
    # so a method that dumps selected variables is needed.
    def compute_hash(self) -> str:
        self.merkle_root = self.compute_merkle_root()
        # Hash with index, timestamp, previous_hash, merkle_root, nonce
        # Hash without transacitons
        payload = str(self.to_dict()).encode()
        return sha256(payload).hexdigest()

    # ------------------------------------------------------------------------------------------------------------------
    # New methods beyond EE4017 labs

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
            b = leaves[index + 1] if index + 1 < len(leaves) else leaves[index]
            root = self.hash_sum(a, b)
            roots.append(root)
            index += 2

        return self.merkleRoot(roots)
