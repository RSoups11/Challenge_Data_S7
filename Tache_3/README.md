## pipeline.py

#### Les arguments
Le script python attend en argument lors de son appel en ligne de commande, un type d'attribut entre **'features'** et **'graphfeatures'** puis un type d'anomalies parmis **'leaks'**, **'outages'**, **'hijack'**. 

**Exemple** : *python pipeline.py graphfeatures outages*

#### Utilisation des arguments
Ensuite, les données sans anomalie correspondantes vont être charger en meme temps que les données liées à l'anomalie choisie.
Après chargement des données, on va retirer les colonnes constantes des dataframes et on ne va considérer que les colonnes en communs.

#### Entrainement et évaluation
Un split en 80/20 - entrainement/test des données. Un gridsearch est effectué pour trouver les meilleurs paramètres pour chaque modèle. Ensuite lorsque les meilleurs paramètres sont trouvé des prédictions sont faites. Cela est effectué 30 fois pour un calcul d'ecart type.

#### Traitement
La normalisation se fait dans un premier temps sur les données d'entrainement puis le meme scaler est utilisé sur les données de test. 

#### Production
Un fichier csv contenant les résultats par rapport aux métriques d'évaluation par modèle (DT, NB, KNN) est produit à l'emplacement du fichier .py

## pipeline_chi2.py

Semblable au pipeline normal sauf qu'ici une selection des 5 meilleurs attributs par chi_2 se fait à la suite de la normalisation sur les données de test avec les labels. Le selector est appliqué aux données de test ensuite pour avoir les mêmes colonnes.

## run.bat 

Script sous windows pour lancer pipeline_chi2.py avec toute les combinaisons d'arguments possibles en renommant les csv à chaque fois.