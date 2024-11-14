import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
import argparse

def load_data(type, attribute):
    return pd.read_csv(f"../Tache_1/{type}/{attribute}.csv")


def remove_constante(df):
    '''
        Vérifie tout le dataframe par rapport à la première ligne
        L'inégalité vérifie si les valeurs d'une colonne varient 
        (cad : Si la valeur de la colonne à la première ligne est au moin différent une fois sur une autre ligne)
        Cela donne un masque booléen (un dataframe de True/False)
        any() est ensuite utilise pour checker sur chaque colonne si il y a au moin 1 True (colonne non constante)
        Renvoie True si c'est le cas, False sinon
        Finalement on ne garde que les colonnes True (cela enlève les colonnes constantes)
    '''
    return df.loc[:, (df != df.iloc[0]).any()]

def minmax(data):
    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(data)
    return pd.DataFrame(data_normalized, columns=data.columns)

def chi_2(data1, data2, k=5):
    # Considère uniquement les colonnes communes aux deux DataFrames
    commun = data1.columns.intersection(data2.columns)
    data1 = data1[commun]
    data2 = data2[commun]

    # Concatène les deux jeux de données pour une normalisation cohérente
    combined_data = pd.concat([data1, data2], ignore_index=True)
    combined_data = minmax(combined_data)  # Normalisation des données combinées
    labels = np.array([0] * len(data1) + [1] * len(data2))

    # Vérification des NaN
    if combined_data.isnull().values.any():
        print("Attention : Valeurs NaN")
    
    # Sélection des attributs avec chi2
    selector = SelectKBest(chi2, k=k)
    selector.fit(combined_data, labels)
    selected_features = combined_data.columns[selector.get_support(indices=True)]
    
    # Séparation des données normalisées après sélection des features
    no_anomaly = combined_data.iloc[:len(data1)][selected_features]
    anomaly = combined_data.iloc[len(data1):][selected_features]
    
    return no_anomaly, anomaly, selected_features

# Visualisation
def plot_boxplots(data1, data2, selected_features, attribute_type, anomaly_type):
    # Combine les données avec une colonne pour distinguer les deux types
    data_combined = pd.concat([data1.assign(Type='no_anomaly'), data2.assign(Type=anomaly_type)], ignore_index=True)
    
    # Transforme les données pour un format dapté aux boxplots [Type, Variable, Valeur]
    data_melted = data_combined.melt(id_vars=['Type'], value_vars=selected_features, var_name='Attribut', value_name='Valeur normalisée')
    
    # Création du boxplot
    plt.figure(figsize=(12, 10))
    sns.boxplot(x='Attribut', y='Valeur normalisée', hue='Type', data=data_melted)
    plt.title(f'Boxplot des 5 meilleurs attributs : {attribute_type} - {anomaly_type}')
    plt.xlabel('Attributs')
    plt.ylabel('Valeur normalisée')
    plt.xticks(rotation=45)
    plt.legend(title='Type')
    plt.tight_layout()
    plt.show()

# Main
def analyze_data(attribute_type, anomaly_type):
    # Charge les données sans anomalies
    no_anomaly = load_data(attribute_type, "no_anomaly")

    # Charge les données d'anomalies
    anomaly = load_data(attribute_type, anomaly_type)
    
    # Remove constant columns
    no_anomaly = remove_constante(no_anomaly)
    anomaly = remove_constante(anomaly)

    # Select k best features
    no_anomaly_best, anomaly_best, selection = chi_2(no_anomaly, anomaly)

    # Visualization
    plot_boxplots(no_anomaly_best, anomaly_best, selection, attribute_type, anomaly_type)

# Permet de mettre les arguments en ligne de commande
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyse et traitement de donnée d\'anomalie BGP')

    # Force l'ajout d'argument 'attribute_type' et 'anomaly_type' lors de l'appel du script
    parser.add_argument('attribute_type', type=str, help='Type d\'attribut (features ou graphfeatures)')
    parser.add_argument('anomaly_type', type=str, help='Type d\'anomalie (leaks, outages, hijack)')

    # Parse la commande pour mettre les arguments dans args
    args = parser.parse_args()
    
    # Run le script avec les entrées utilisateurs stocké dans args
    analyze_data(args.attribute_type, args.anomaly_type)
