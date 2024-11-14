import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.feature_selection import SelectKBest, chi2
import argparse

def load_data(atype, attribute):
    return pd.read_csv(f"../Tache_1/{atype}/{attribute}.csv")

def remove_constante(df):
    return df.loc[:, (df != df.iloc[0]).any()]

def split_minmax(data_train, data_test):
    scaler = MinMaxScaler()
    data_train_normalized = scaler.fit_transform(data_train)
    data_test_normalized = scaler.transform(data_test)
    return pd.DataFrame(data_train_normalized, columns=data_train.columns), pd.DataFrame(data_test_normalized, columns=data_test.columns)

def split_chi_2(data_train, labels, data_test, k=5):
    # Sélection des attributs avec chi2
    selector = SelectKBest(chi2, k=k)
    data_train_select = selector.fit_transform(data_train, labels)
    data_test_select = selector.transform(data_test)
    selected_features = data_train.columns[selector.get_support(indices=True)]
    
    return pd.DataFrame(data_train_select, columns=selected_features), pd.DataFrame(data_test_select, columns=selected_features)

def train_and_evaluate(attribute_type, anomaly_type):
    # Charge les données
    no_anomaly = load_data(attribute_type, "no_anomaly")
    anomaly = load_data(attribute_type, anomaly_type)

    # Enlève les colonnes constantes
    no_anomaly = remove_constante(no_anomaly)
    anomaly = remove_constante(anomaly)

    # Garde uniquement les colonnes communes aux deux dataframe
    commun = no_anomaly.columns.intersection(anomaly.columns)
    no_anomaly = no_anomaly[commun]
    anomaly = anomaly[commun]

    # Concatène les données et les étiquettes
    X = pd.concat([no_anomaly, anomaly], ignore_index=True)
    Y = np.array([0] * len(no_anomaly) + [1] * len(anomaly))
    
    # Initialise les modèles et leurs paramètres
    models = {
        'Decision Tree': (
            DecisionTreeClassifier(),
            {
                'criterion': ['gini', 'entropy'], 
                'max_depth': [3, 5, 10],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2']
            }
        ),
        'Naive Bayes': (
            GaussianNB(),
            {}
        ),
        'KNN': (
            KNeighborsClassifier(),
            {
                'n_neighbors': [3, 5, 7],
                'weights': ['uniform', 'distance']
            }
        )
    }
    
    # Stock les scores
    results = {
        model_name: {
            'train_accuracy': [], 'test_accuracy': [],
            'train_precision': [], 'test_precision': [],
            'train_recall': [], 'test_recall': []
        } 
        for model_name in models
    }

    # Stock les meilleurs paramètres
    best_params = {model_name: [] for model_name in models}
    
    for _ in range(30):
        
        # Train/Test Split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        # Normalisation de l'ensemble d'entraînement et application sur l'ensemble de test
        X_train_normalized, X_test_normalized = split_minmax(X_train, X_test)

        # Sélection des meilleurs attributs avec chi2 sur les données normalisées
        X_train_selected, X_test_selected = split_chi_2(X_train_normalized, Y_train, X_test_normalized)
        
        for model_name, (model, params) in models.items():
            # Recherche des meilleurs hyperparamètres avec GridSearch
            grid = GridSearchCV(model, params, scoring='accuracy', cv=5)
            grid.fit(X_train_selected, Y_train)
            best_model = grid.best_estimator_

            # Ajoute les meilleurs paramètres trouvé à chaque fois
            best_params[model_name].append(grid.best_params_)
            
            # Prédictions
            Y_pred_train = best_model.predict(X_train_selected)
            Y_pred_test = best_model.predict(X_test_selected)
            
            # Calcul des métriques
            results[model_name]['train_accuracy'].append(accuracy_score(Y_train, Y_pred_train))
            results[model_name]['test_accuracy'].append(accuracy_score(Y_test, Y_pred_test))
            results[model_name]['train_precision'].append(precision_score(Y_train, Y_pred_train))
            results[model_name]['test_precision'].append(precision_score(Y_test, Y_pred_test))
            results[model_name]['train_recall'].append(recall_score(Y_train, Y_pred_train))
            results[model_name]['test_recall'].append(recall_score(Y_test, Y_pred_test))


    # Affiche les meilleurs paramètres par modèles
    '''
    for model_name, params_list in best_params.items():
        print(f"\nMeilleurs paramètres pour {model_name} :")
        for i, params in enumerate(params_list, 1):
            print(f"  Repetition {i}: {params}")
    '''

    with open("best_params_chi2.txt", "w") as f:
        for model_name, params_list in best_params.items():
            f.write(f"\nMeilleurs parametres pour {model_name} :\n")
            for i, params in enumerate(params_list, 1):
                f.write(f"  Repetition {i}: {params}\n")

    # Calcul des moyennes et écarts types
    description = []
    for model_name, metrics in results.items():
        # Une ligne pour chaque modèle et chaque métrique (Moyenne ± Écart-Type)
        description.append({
            'Model': model_name,
            'Train Accuracy': f"{np.mean(metrics['train_accuracy']):.3f} ± {np.std(metrics['train_accuracy']):.3f}",
            'Test Accuracy': f"{np.mean(metrics['test_accuracy']):.3f} ± {np.std(metrics['test_accuracy']):.3f}",
            'Train Precision': f"{np.mean(metrics['train_precision']):.3f} ± {np.std(metrics['train_precision']):.3f}",
            'Test Precision': f"{np.mean(metrics['test_precision']):.3f} ± {np.std(metrics['test_precision']):.3f}",
            'Train Recall': f"{np.mean(metrics['train_recall']):.3f} ± {np.std(metrics['train_recall']):.3f}",
            'Test Recall': f"{np.mean(metrics['test_recall']):.3f} ± {np.std(metrics['test_recall']):.3f}"
        })
    
    # Création du DataFrame
    df_results = pd.DataFrame(description)
    
    # Ajustement de l'ordre des colonnes
    df_results = df_results[
        [
            'Model', 
            'Train Accuracy', 'Test Accuracy', 
            'Train Precision', 'Test Precision', 
            'Train Recall', 'Test Recall'
        ]
    ]
    
    # Sauvegarder en CSV
    df_results.to_csv('model_performance_chi2.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Entrainement et évaluation')
    parser.add_argument('attribute_type', type=str, help='Type d\'attribut (Features ou GraphFeatures)')
    parser.add_argument('anomaly_type', type=str, help='Type d\'anomalie (leaks, outages, hijack)')
    args = parser.parse_args()
    
    train_and_evaluate(args.attribute_type, args.anomaly_type)