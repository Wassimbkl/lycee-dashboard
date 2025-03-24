import pandas as pd


file1 = "Data/annuaire-de-leducation.csv"
file2 = "Data/fr-en-indicateurs-de-resultat-des-lycees-gt_v2.csv"

df1 = pd.read_csv(file1, sep=';', encoding='utf-8')
df2 = pd.read_csv(file2, sep=';', encoding='utf-8')

print("Colonnes du fichier Annuaire de l'Éducation :")
print(df1.columns.tolist())

print("\nColonnes du fichier Indicateurs de Résultats des Lycées :")
print(df2.columns.tolist())
