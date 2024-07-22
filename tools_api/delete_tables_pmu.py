import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
import os

LAST_RUN_FILE = 'last_run_date.txt'

def delete_tables_pmu():
    # Connexion à la base de données
    engine = create_engine('postgresql://admin:admin@localhost:5434/bdd_equide')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Définir les tables avec respect de l'ordre des dépendances
        tables = [
            "participations_aux_courses",
            "courses",
            "reunion",
            "programmes_des_courses"
        ]

        # Truncate tables en respectant l'ordre
        for table_name in tables:
            session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE'))

        # Commit des changements
        session.commit()

        # Supprimer le fichier last_run_date.txt s'il existe
        if os.path.exists(LAST_RUN_FILE):
            os.remove(LAST_RUN_FILE)
        
        message = "Les tables ont été purgées avec succès, les identifiants ont été réinitialisés et le fichier last_run_date.txt a été supprimé."
    except Exception as e:
        # Rollback en cas d'erreur
        session.rollback()
        message = f"Erreur lors de la suppression des tables: {str(e)}"
    finally:
        session.close()

    return message