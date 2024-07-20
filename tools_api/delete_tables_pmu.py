import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

def delete_tables_pmu():
    # Connexion à la base de données
    engine = create_engine('postgresql://admin:admin@localhost:5434/bdd_equide')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Récupérer les métadonnées
        meta = MetaData()
        meta.reflect(bind=engine)

        # Définir les tables avec respect de l'ordre des dépendances
        tables = [
            "participations_aux_courses",
            "courses",
            "reunion",
            "programmes_des_courses"
        ]

        # Supprimer le contenu des tables en respectant l'ordre
        for table_name in tables:
            table = Table(table_name, meta, autoload_with=engine)
            session.execute(table.delete())
        
        # Commit des changements
        session.commit()
        message = "Les tables ont été purgées avec succès"
    except Exception as e:
        # Rollback en cas d'erreur
        session.rollback()
        message = f"Erreur lors de la suppression des tables: {str(e)}"
    finally:
        session.close()

    return message
