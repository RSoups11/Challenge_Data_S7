# Challenge Data - Esiroi - 4A-IT Promo 2026 - S7

Ce dépôt contient les différentes taches effectuées lors du challenge data présenté par monsieur Hoarau Kevin dans le cour de Data et IA de l'Esiroi.

## Les dossiers Tache_x 

### Tache_1 

tache1.py contient les traitements utilisé pour récupérer les données BGP sur un cluster HDFS afin de produire des csv

### Tache_2

traitement.py est un script permettant de faire des traitements sur les csv précedemment créé (Nettoyage de constante, normalisation, selection d'attribut par chi2) pour faire un affichage box_plot entre des données d'anomalies (leaks, outages, hijack) en confrontation avec des données sans anomalie en fonction du type d'attribut (Features ou GraphFeatures).

### Tache_3

pipeline.py et pipeline_chi2.py sont des scripts python permettant la mise en place d'un pipeline d'apprentissage automatique pour une combinaison type d'attribut et anomalie. Les modèles testé sont : Arbre de décision, K-NN, Bayesien Naif. 

pipeline_chi2 implémente aussi la selection des 5 meilleurs attributs par le chi2 par découpage des données.  
