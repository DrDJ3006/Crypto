import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization



class Blockchain:
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof: int, previous_hash: Optional[str] = None) -> Dict[str, Any]:
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Dict[str, Any]:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Exemple d'utilisation
blockchain = Blockchain()
last_proof = blockchain.last_block['proof']
proof = blockchain.proof_of_work(last_proof)

# Ajout d'un nouveau bloc à la blockchain
previous_hash = blockchain.hash(blockchain.last_block)
block = blockchain.new_block(proof, previous_hash)

previous_hash = blockchain.hash(blockchain.last_block)
block = blockchain.new_block(proof, previous_hash)

print("Blockchain:", blockchain.chain)
