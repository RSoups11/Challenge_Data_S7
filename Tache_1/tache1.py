from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, avg, stddev, median
import os


# Création d'une instance Spark

spark = SparkSession.builder.appName("Extraction des features").getOrCreate()


# Fonction d'extraction
def extraction(df, attributes):
    # Calcul des statistiques pour chaque attribut dans chaque échantillon
    aggregations = []
    for attribute in attributes:
        aggregations.extend([
            min(attribute).alias(f"{attribute}_min"),
            max(attribute).alias(f"{attribute}_max"),
            avg(attribute).alias(f"{attribute}_avg"),
            stddev(attribute).alias(f"{attribute}_std"),
            median(attribute).alias(f"{attribute}_median")
        ])
    return df.agg(*aggregations) # Utilise * pour considérer chaque élément de la liste d'aggregations comme un argument distinct dans df.agg()



# Fonction de traitement principal
def traitement_data(data, dtype="Features"):
    # Chemin HDFS vers les données échantillon
    path = f"hdfs://localhost:9000/shared/data/{data}/*/transform/{dtype}/*.json"
    
    # Chemins de chaque échantillon (récupère le premier élément de la paire (chemin, contenu))
    sample_paths = spark.sparkContext.wholeTextFiles(path).keys().collect()

    # DataFrame pour accumuler les résultats de chaque échantillon
    results = None

    # Calcul des statistiques pour chaque échantillon (chaque dossier de timestamp)
    for sample_path in sample_paths:
        # Un fichier JSON pour un échantillon
        df_sample = spark.read.json(sample_path)
        
        # Liste des attributs dans le fichier
        attributes = df_sample.columns  
        
        # Calcul pour l'échantillon
        stats = extraction(df_sample, attributes)
        
        # Ajout des résultats au DataFrame final
        results = stats if results is None else results.union(stats)

    # Chemin de sauvegarde des résultats
    output_path = f"hdfs://localhost:9000/user/jupyter-raphael.soupaya/data_{dtype}/{data}"
    
    # Sauvegarde des résultats en CSV
    results.coalesce(1).write.csv(output_path, header=True, mode="overwrite") # coalesce(1) pour forcer Spark à produire un unique fichier csv (évite un genre de partionnement)


# Exécution de l'extraction pour chaque type d'anomalie
data_types = ["leaks", "outages", "hijack", "no_anomaly"]
for data_type in data_types:
    # Extraction pour les features
    # traitement_data(data_type, dtype="Features")
    # Extraction pour les graphes
    traitement_data(data_type, dtype="GraphFeatures")

# Fermeture de la session
spark.stop()
