import numpy as np

def gen_key():
    """
    Génère la clé publique et privée.
    """
    # Bonne matrice de base du treillis B (2x2 pour simplifier)
    B = np.array([[1, 0], [0, 1]])

    # Matrice U de déterminant 1 avec de grandes entrées
    U = np.array([[2, 3], [1, 2]])  # Exemple

    # Calcul de B'
    B_prime = np.matmul(B, U)

    # La clé publique est B', la clé privée est (B, U)
    return B_prime, (B, U)

def encrypt(B_prime, m):
    """
    Chiffre le message m avec la clé publique B_prime.
    """
    # Calcul de B'm
    c = np.dot(B_prime, m)

    # Ajout d'un vecteur aléatoire e
    e = np.random.rand(2)  # Vecteur aléatoire simple
    c += e

    return c

def decrypt(B, U, c):
    """
    Déchiffre le message c avec la clé privée (B, U).
    """
    # Calcul de B^-1c
    d = np.dot(np.linalg.inv(B), c)

    # Arrondissement pour obtenir d'
    d_prime = np.round(d)

    # Calcul de U^-1d'
    m_decoded = np.dot(np.linalg.inv(U), d_prime)

    return m_decoded

# Exemple d'utilisation
B_prime, (B, U) = gen_key()
m = np.array([5, 3])  # Message à chiffrer
c = encrypt(B_prime, m)

print("Message chiffré:", c)

m_decoded = decrypt(B, U, c)
print("Message déchiffré:", m_decoded)
