# =====================================================
# PROJET : Analyse Automatisée des Ventes
# AUTEURS : Ikbel Jadlaoui & Yasmin Aouadhi
# CLASSE : LMI 2 - FST
# =====================================================
import csv
import matplotlib.pyplot as plt

# =====================================================
# 1. GÉNÉRATION AUTOMATIQUE DU FICHIER ventes.csv
# =====================================================
donnees_initiales = [
    {"ID": "101", "Prix": "15.0", "Quantite": "3", "Remise": "10"},
    {"ID": "102", "Prix": "25.0", "Quantite": "2", "Remise": "5"},
    {"ID": "103", "Prix": "10.0", "Quantite": "5", "Remise": "0"}
]

with open("ventes.csv", mode="w", newline="", encoding="utf-8") as f_init:
    writer_init = csv.DictWriter(f_init, fieldnames=["ID", "Prix", "Quantite", "Remise"])
    writer_init.writeheader()
    writer_init.writerows(donnees_initiales)

print("Fichier 'ventes.csv' généré automatiquement.")

# =====================================================
# 2. INITIALISATION DES VARIABLES
# =====================================================
donnees_finales = []
ca_total_net = 0
max_benefice = 0
id_produit_phare = ""

# =====================================================
# 3. LECTURE ET TRAITEMENT DES DONNÉES
# =====================================================
with open("ventes.csv", mode="r", encoding="utf-8") as fichier:
    lecteur = csv.DictReader(fichier)

    for ligne in lecteur:
        id_prod = ligne["ID"]
        prix = float(ligne["Prix"])
        quantite = int(ligne["Quantite"])

        # Nettoyage de la remise (garde uniquement les chiffres)
        valeur_nettoyee = "".join(c for c in ligne["Remise"] if c.isdigit())
        remise = float(valeur_nettoyee) if valeur_nettoyee else 0.0

        # Calculs
        ca_brut = prix * quantite
        ca_net = ca_brut * (1 - remise / 100)
        tva = ca_net * 0.2

        # Accumulation du CA total
        ca_total_net += ca_net

        # Détection du produit phare
        if ca_net > max_benefice:
            max_benefice = ca_net
            id_produit_phare = id_prod

        # Ajout des résultats enrichis
        ligne["CA_Brut"] = round(ca_brut, 2)
        ligne["CA_Net"] = round(ca_net, 2)
        ligne["TVA"] = round(tva, 2)

        donnees_finales.append(ligne)

# =====================================================
# 4. AFFICHAGE DES RÉSULTATS DANS LA CONSOLE
# =====================================================
print("-" * 30)
print(f"CA Total Net : {round(ca_total_net, 2)} DT")
print(f"Produit Phare (ID) : {id_produit_phare}")
print("-" * 30)

# =====================================================
# 5. EXPORT DES RÉSULTATS EN CSV
# =====================================================
if donnees_finales:
    with open("resultats_final.csv", mode="w", newline="", encoding="utf-8") as f:
        champs = donnees_finales[0].keys()
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(donnees_finales)

    print("Fichier 'resultats_final.csv' créé avec succès ✅")

    # =====================================================
    # 6. VISUALISATION GRAPHIQUE
    # =====================================================
    ids = [str(d['ID']) for d in donnees_finales]
    ca_nets = [d['CA_Net'] for d in donnees_finales]

    plt.figure(figsize=(10, 6))
    plt.bar(ids, ca_nets, color='skyblue')

    plt.title("Chiffre d'Affaires Net par Produit")
    plt.xlabel("ID du Produit")
    plt.ylabel("CA Net (DT)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()

else:
    print("Erreur : Aucune donnée à traiter ❌")