import os
import pandas as pd

# Répertoires de téléchargement et de sortie
download_dir = r"C:\Users\39812\OneDrive - Aix Marseille Provence Métropole\Documents\Bike Project\Datasets_preparation"
Dataset = r"C:\Users\39812\OneDrive - Aix Marseille Provence Métropole\Documents\Bike Project\Datasets"

# Liste pour stocker les DataFrames de chaque fichier CSV
dfs = []

# Récupérer tous les fichiers CSV dans le répertoire de téléchargement
csv_files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]

# Trier les fichiers par date extraite du nom de fichier
csv_files.sort(key=lambda x: x.split('~')[1].split('.')[0])

# Lire chaque fichier CSV, ajouter la colonne "Dates" et ajouter le DataFrame à la liste
for csv_file in csv_files:
    file_path = os.path.join(download_dir, csv_file)
    df = pd.read_csv(file_path)
    
    # Extraire la date du nom de fichier
    date_str = csv_file.split('~')[1].split('.')[0]
    
    # Ajouter la colonne "Dates"
    df.insert(0, "Dates", date_str)
    
    # Ajouter le DataFrame à la liste
    dfs.append(df)

# Concaténer tous les DataFrames dans la liste en un seul DataFrame
combined_df = pd.concat(dfs, ignore_index=True)

# Enregistrer le DataFrame combiné dans un fichier CSV dans le répertoire de sortie
output_file = os.path.join(Dataset, "Data.csv")
combined_df.to_csv(output_file, index=False)

print(f"Le fichier Data.csv a été créé avec succès et enregistré dans {Dataset}")