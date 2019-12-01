import json
from hashlib import sha256
from typing import List

from Crypto.Hash import SHA

from pycoin import Transaction

class Block:
    def __init__(self, index: int, transaction: List[Transaction], timestamp: str, previous_hash: str):
        self.index: int = index
        self.transaction: List[Transaction] = transaction
        self.timestamp: str = timestamp
        self.previous_hash: str = previous_hash
        self.hash: str = "0"
        self.nonce: int = 0

    def to_dict(self) -> dict:
        return {
            'index': self.index,
            'transaction': self.transaction,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=False)

    def compute_hash(self) -> str:
        payload = str(self.to_dict()).encode()
        return sha256(payload).hexdigest()
