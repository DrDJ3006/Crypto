import hashlib
import json
from time import time
from typing import Any, Dict, List, Optional
from random import choice

class Blockchain:
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        self.stake: Dict[str, int] = {}  # stocke la participation de chaque utilisateur
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, node_identifier: str) -> None:
        self.stake[node_identifier] = 1  # ou une autre logique pour attribuer des participations initiales

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

    def proof_of_stake(self) -> str:
        total_stake = sum(self.stake.values())
        stake_choices = [(node, stake / total_stake) for node, stake in self.stake.items()]
        chosen_node, _ = choice(stake_choices)  # Choix aléatoire pondéré en fonction des participations
        return chosen_node

    def validate_block(self, node_identifier: str, proof: int) -> bool:
        # Ici, vous pouvez ajouter votre logique de validation de bloc,
        # comme vérifier si le validateur a la participation requise.
        return True

# Exemple d'utilisation
blockchain = Blockchain()
blockchain.register_node("node_A")
blockchain.register_node("node_B")

# Sélection du validateur
chosen_node = blockchain.proof_of_stake()
proof = 12345  # Ce serait le résultat d'une sorte de calcul ou d'algorithme spécifique à votre blockchain

# Validation et ajout du bloc
if blockchain.validate_block(chosen_node, proof):
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

print("Blockchain:", blockchain.chain)
    