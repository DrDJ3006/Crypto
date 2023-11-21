class SmartContract:
    def __init__(self):
        self.balances = {"Alice": 100, "Bob": 100}  # Soldes initiaux
        self.bet_amount = 10  # Montant du pari
        self.bet_from_Alice = None
        self.bet_from_Bob = None
        self.match_result = None  # Résultat du match

    def bet(self, player, team):
        if self.balances[player] < self.bet_amount:
            return f"{player} n'a pas assez de fonds pour parier."
        self.balances[player] -= self.bet_amount
        if player == "Alice":
            self.bet_from_Alice = team
        else:
            self.bet_from_Bob = team
        return f"{player} a parié {self.bet_amount} sur {team}."

    def set_match_result(self, result):
        self.match_result = result
        self.settle_bet()

    def settle_bet(self):
        if not self.match_result or not self.bet_from_Alice or not self.bet_from_Bob:
            return "Le pari ne peut pas encore être réglé."
        winner = None
        if self.bet_from_Alice == self.match_result:
            winner = "Alice"
        elif self.bet_from_Bob == self.match_result:
            winner = "Bob"
        
        if winner:
            self.balances[winner] += self.bet_amount * 2
            return f"{winner} a gagné le pari!"
        return "Pas de gagnant pour ce pari."

# Utilisation du contrat intelligent
contract = SmartContract()
print(contract.bet("Alice", "Équipe A"))
print(contract.bet("Bob", "Équipe B"))
print(contract.set_match_result("Équipe A"))  # Résultat du match
print(contract.balances)  # Afficher les soldes après le pari
