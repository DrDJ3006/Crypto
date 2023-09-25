# Paramètres
seuil = 3  # Le seuil nécessaire pour reconstituer la clé
parts_de_cle = [(2, 154), (3, 33), (5, 208)]  # Exemple de parties de clé (x, y)

# Fonction pour reconstituer la clé secrète
def reconstituer_cle_secrete(parts_de_cle, seuil, prime):
    cle_reconstituee = 0
    for i in range(seuil):
        xi, yi = parts_de_cle[i]
        produit = yi
        for j in range(seuil):
            if j != i:
                xj, yj = parts_de_cle[j]
                xj_inv = pow(xi - xj, -1, prime)
                produit = (produit * xj * xj_inv) % prime
        cle_reconstituee = (cle_reconstituee + produit) % prime
    return cle_reconstituee

# Document à signer (exemple)
document = "Ceci est un document à signer."

# Clé secrète reconstituée
prime = 257  # Utiliser le même nombre premier que lors de la génération des parts
cle_secrete = reconstituer_cle_secrete(parts_de_cle, seuil, prime)
# Signature du document
signature = hash(document + str(cle_secrete))  # Une signature simple avec hachage

# Affichage de la signature
print(f"Signature du document : {signature}")
