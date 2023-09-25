import random

# Fonction pour générer un polynôme aléatoire
def generer_polynome(secret_key, seuil, nombre_de_parts, prime):
    coef = [secret_key]
    for _ in range(seuil - 1):
        coef.append(random.randint(1, prime - 1))
    print(coef)
    return coef

# Fonction pour évaluer un polynôme en un point x
def evaluer_polynome(coef, x, prime):
    y = 0
    for i, a in enumerate(coef):
        y += a * (x ** i)
        y %= prime
    return y

# Paramètres
secret_key = 42  # La clé secrète que vous voulez partager
seuil = 3        # Le seuil nécessaire pour reconstituer la clé
nombre_de_parts = 5  # Le nombre total de parts à générer
prime = 257      # Un nombre premier suffisamment grand pour la sécurité

# Génération du polynôme
coef = generer_polynome(secret_key, seuil, nombre_de_parts, prime)

# Génération des parts de clé
parts_de_cle = []
for x in range(1, nombre_de_parts + 1):
    y = evaluer_polynome(coef, x, prime)
    parts_de_cle.append((x, y))

# Affichage des parts de clé
for x, y in parts_de_cle:
    print(f"Partie {x}: {y}")

# Vous pouvez ensuite stocker ces parts de clé en toute sécurité et les distribuer aux membres du groupe.
