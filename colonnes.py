import pandas as pd

# Remplacez par les chemins de vos fichiers
file1 = "Data/annuaire-de-leducation.csv"
file2 = "Data/fr-en-indicateurs-de-resultat-des-lycees-gt_v2.csv"

# Charger les fichiers et afficher les colonnes
df1 = pd.read_csv(file1, sep=';', encoding='utf-8')  # Changez le séparateur si besoin
df2 = pd.read_csv(file2, sep=';', encoding='utf-8')

print("Colonnes du fichier Annuaire de l'Éducation :")
print(df1.columns.tolist())

print("\nColonnes du fichier Indicateurs de Résultats des Lycées :")
print(df2.columns.tolist())
