## traitement.py

#### Les arguments
Le script python attend en argument lors de son appel en ligne de commande, un type d'attribut entre **'features'** et **'graphfeatures'** puis un type d'anomalies parmis **'leaks'**, **'outages'**, **'hijack'**. 

**Exemple** : *python traitement.py graphfeatures outages*

#### Utilisation des arguments
Ensuite, les données sans anomalie correspondantes vont être charger en meme temps que les données liées à l'anomalie choisie.

#### Traitement
A partir des arguments, certains traitements vont être éffectués sur les données dans les csv présents dans les dossiers Tache_1/Features et Tache_1/GraphFeatures.

Les traitements sont dans l'ordre, un nettoyage des colonnes constantes, une normalisation MinMax sur la combinaison des deux jeux de données, une recherche des meilleurs attributs via le chi2 puis un affichage box_plots de ces attributs pour comparer les données sans anomalie vs avec anomalies.