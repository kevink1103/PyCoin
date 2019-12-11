from Crypto.Hash import SHA
from hashlib import sha256
import json


class Block:
    def __init__(self, index, transaction, timestamp, previous_hash):
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = '0'
        self.nonce = 0

    def to_dict(self):
        return {
            'index': self.index,
            'transaction': self.transaction,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
    
    def to_json(self):
        return json.dumps(self.__dict__)

    def compute_hash(self):
        payload = str(self.to_dict()).encode()
        return sha256(payload).hexdigest()
