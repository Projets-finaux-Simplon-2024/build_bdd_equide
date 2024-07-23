# |---------------------------------------------------------- IMPORTS -------------------------------------------------------------------------|
# Libs
import webview
from screeninfo import get_monitors
from flask import Flask, render_template, request, make_response

# Outils
import threading
import os
import subprocess
import sys
import psycopg2
import pandas as pd
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from psycopg2 import sql
from datetime import datetime

# Local
from tools_scraping.recup_annees import recup_annees
from tools_scraping.calcul_nb_pages import calcul_nb_pages
from tools_scraping.con_ifce import connexion_ifce
from tools_scraping.scraping_chevaux_infos_generales import scraping_chevaux_infos_generales
from tools_api.calls_api import call_api
from tools_api.delete_tables_pmu import delete_tables_pmu
from tools_api.tables_pleines import tables_pleines

# |--------------------------------------------------------------------------------------------------------------------------------------------|

app = Flask(__name__)

# Initialisation de la variable globale
list_annees = None

# |---------------------------------------------------------- PAGE ACCUEIL --------------------------------------------------------------------|
@app.route("/")
def index():
    # Check if the container already exists
    inspect_result = subprocess.run(["docker", "inspect", "container_equide"], capture_output=True, text=True)
    
    if inspect_result.returncode == 0:
        subprocess.run(["docker", "start", "container_equide"], capture_output=True, text=True)
    
    return render_template('page_index.html')
# |--------------------------------------------------------------------------------------------------------------------------------------------|




# |---------------------------------------------------------- OUVRIR DOSSIER ------------------------------------------------------------------|
@app.route('/ouvrir_dossier')
def ouvrir_dossier():
    # Obtenez le chemin absolu du dossier 'resultats' relatif à la racine du projet
    chemin_projet = os.path.dirname(os.path.abspath(__file__))
    chemin_dossier = os.path.join(chemin_projet, 'resultats')
    
    # Ouvrir le dossier avec l'explorateur de fichiers natif du système d'exploitation
    if sys.platform == 'win32':
        subprocess.Popen(['explorer', chemin_dossier])
    elif sys.platform == 'darwin':  # macOS
        subprocess.Popen(['open', chemin_dossier])
    else:  # Linux et variantes
        subprocess.Popen(['xdg-open', chemin_dossier])
    
        # Créer une réponse qui inclut un script JavaScript pour rediriger après 3 secondes
    response = make_response("""
    <html>
        <head>
            <meta http-equiv="refresh" content="3;url=/scraping_chevaux_bases" />
        </head>
        <body>
            <p>Dossier ouvert.
        Vous serez redirigé dans quelques secondes...</p>
        </body>
    </html>
    """)
    return response
# |--------------------------------------------------------------------------------------------------------------------------------------------|





# |---------------------------------------------------------- PAGE DE SCRAPING DE BASE --------------------------------------------------------|
@app.route("/scraping_chevaux_bases", methods=['GET', 'POST'])
def scraping_chevaux_bases():
    global list_annees

    if not list_annees:
        list_annees = recup_annees()

    dossier = 'resultats'
    fichiers = []
    for f in os.listdir(dossier):
        if f.startswith('donnees_chevaux_'):
            file_path = os.path.join(dossier, f)
            stat = os.stat(file_path)
            fichiers.append({
                'nom': f,
                'taille': stat.st_size/1000,  # Taille du fichier en kilo-octets
                'date_modification': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),  # Dernière modification
                'date_creation': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')  # Date de création
            })

    context = {
        'list_annees': list_annees,
        'fichiers':fichiers
    }

    if request.method == 'POST':
        action = request.form['action']

        # Récupérer les années sélectionnées dans le formulaire
        annees = request.form.getlist('annees[]')

        driver = connexion_ifce()

        # Appeler la fonction pour obtenir les informations supplémentaires
        nombre_chevaux, nombre_pages = calcul_nb_pages(driver, annees)

        # Temps de scraping par page en secondes
        temps_par_page = 3.5

        # Calculer le temps total en secondes
        temps_total_secondes = nombre_pages * temps_par_page

        # Convertir le temps total en heures, minutes et secondes
        heures = temps_total_secondes // 3600
        minutes = (temps_total_secondes % 3600) // 60
        secondes = temps_total_secondes % 60

        # Afficher les résultats
        print('\n---------------------------------------------------------------------------------------------------------------------------------')
        print(f"Nombre de chevaux : {nombre_chevaux}")
        print(f"Nombre de pages : {nombre_pages}")
        print(f"Temps total estimé pour le scraping (pour 3.5s par page de 100 articles): {heures} heures {minutes} minutes {secondes} secondes")
        print('---------------------------------------------------------------------------------------------------------------------------------\n')

        if action == 'infos':

            # Mettre à jour le contexte avec les informations supplémentaires
            context['nombre_chevaux'] = nombre_chevaux
            context['nombre_pages'] = nombre_pages
            context['heures'] = heures
            context['minutes'] = minutes
            context['secondes'] = secondes
            context['annees'] = annees

            # Rendre le template avec le contexte mis à jour
            return render_template('page_scraping_chevaux_bases.html', **context)
        
        if action == 'scraping':

            nb_chevaux_scrap, duration, fichier_csv = scraping_chevaux_infos_generales(driver, nombre_pages, annees)

            # Convertir le temps total en heures, minutes et secondes
            heures_duration = duration // 3600
            minutes_duration = (duration % 3600) // 60
            secondes_duration = duration % 60

            print(f"Le scraping a pris {heures_duration} heures {minutes_duration} minutes {secondes_duration} secondes.\n")

            # Afficher un message pour confirmer l'enregistrement
            print(f"Les données ont été enregistrées dans le fichier '{fichier_csv}'.\n")

            context['heures'] = heures
            context['minutes'] = minutes
            context['secondes'] = secondes
            context['annees'] = annees
            context['heures_duration'] = heures_duration
            context['minutes_duration'] = minutes_duration
            context['secondes_duration'] = secondes_duration
            context['fichier_csv'] = fichier_csv
            context['nb_chevaux_scrap'] = nb_chevaux_scrap

            return render_template('page_scraping_chevaux_bases.html', **context)

    return render_template('page_scraping_chevaux_bases.html', **context)
# |--------------------------------------------------------------------------------------------------------------------------------------------|


# |---------------------------------------------------------- PAGE DE CREATION DU CONTAINER POSTGRES ------------------------------------------|
@app.route("/creation_container", methods=['GET', 'POST'])
def creation_container():

    if request.method == 'POST':

        action = request.form['action']

        if action == 'retour':
            return render_template('page_index.html')

        if action == 'supprimer':

            # Supprimer le fichier last_run_date.txt s'il existe
            if os.path.exists('last_run_date.txt'):
                os.remove('last_run_date.txt')

            # Stop and remove the PostgreSQL container
            stop_result = subprocess.run(["docker", "stop", "container_equide"], capture_output=True, text=True)
            remove_result = subprocess.run(["docker", "rm", "container_equide"], capture_output=True, text=True)
            
            if stop_result.returncode == 0 and remove_result.returncode == 0:
                message = "La base de données PostgreSQL a été supprimée avec succès."
            else:
                message = f"Erreur lors de la suppression de la base de données PostgreSQL : {stop_result.stderr or remove_result.stderr}"
            
            return render_template('page_creation_container.html', message=message)

        if action == 'creation':
            # Check if the container already exists
            inspect_result = subprocess.run(["docker", "inspect", "container_equide"], capture_output=True, text=True)
            
            if inspect_result.returncode == 0:
                # The container already exists
                error_message = "Un conteneur avec le nom 'container_equide' existe déjà."
                return render_template('page_creation_container.html', error=error_message)
            else:
                # Pull the PostgreSQL image from Docker Hub
                subprocess.run(["docker", "pull", "postgres"])
                
                # Run a new PostgreSQL container
                result = subprocess.run([
                    "docker", "run", "--name", "container_equide", 
                    "-e", "POSTGRES_USER=admin", 
                    "-e", "POSTGRES_PASSWORD=admin", 
                    "-e", "POSTGRES_DB=bdd_equide", 
                    "-p", "5434:5432", 
                    "-d", "postgres"
                ], capture_output=True, text=True)
                
                # Check if the container started successfully
                if result.returncode == 0:
                    container_id = result.stdout.strip()
                    creation_info = {
                        "container_id": container_id,
                        "container_name": "container_equide",
                        "host": "localhost",
                        "port": "5434",
                        "user": "admin",
                        "password": "admin",
                        "database": "bdd_equide"   
                    }
                    return render_template('page_creation_container.html', creation_info=creation_info)
                else:
                    error_message = result.stderr
                    return render_template('page_creation_container.html', error=error_message)
        
    return render_template('page_creation_container.html')
# |--------------------------------------------------------------------------------------------------------------------------------------------|



# |---------------------------------------------------------- PAGE D'IMPLEMENTATION TABLES ----------------------------------------------------|
@app.route("/implementation_tables", methods=['GET', 'POST'])
def implementation_tables():
    # Check if the container is running
    inspect_result = subprocess.run(["docker", "inspect", "--format='{{.State.Running}}'", "container_equide"], capture_output=True, text=True)
    
    if inspect_result.returncode != 0:
        # If the container does not exist
        return render_template('page_no_container.html')
    elif "false" in inspect_result.stdout:
        # If the container is not running
        return render_template('page_container_stopped.html')
    
    if request.method == 'POST':
        action = request.form['action']

        if action == 'retour':
            return render_template('page_index.html')
        
        if action == 'creation':
            try:
                # Connect to the PostgreSQL database
                conn = psycopg2.connect(
                    dbname="bdd_equide",  # Database name
                    user="admin",  # Database user
                    password="admin",  # Database password
                    host="localhost",  # Database host
                    port="5434"  # Database port
                )
                cur = conn.cursor()

                # Lire le fichier SQL
                with open('diagram_equide.sql', 'r') as file:
                    sql = file.read()

                # Exécuter les instructions SQL
                cur.execute(sql)

                # Commit changes
                conn.commit()

                # Close communication with the database
                cur.close()
                conn.close()

                creation_info = "Les tables ont été créées avec succès."
                return render_template('page_implementation_tables.html', creation_info=creation_info)

            except (Exception, psycopg2.DatabaseError) as error:
                return render_template('page_implementation_tables.html', error=str(error))
    
    return render_template('page_implementation_tables.html')
# |--------------------------------------------------------------------------------------------------------------------------------------------|



# |---------------------------------------------------------- PAGE REMPLISSAGE TABLE CHEVAUX TF  ----------------------------------------------|
@app.route("/remplissage_table_chevaux_tf", methods=['GET', 'POST'])
def remplissage_table_chevaux_tf():
    fichiers_uploades = []

    # Check if the container is running
    inspect_result = subprocess.run(["docker", "inspect", "--format='{{.State.Running}}'", "container_equide"], capture_output=True, text=True)
    
    if inspect_result.returncode != 0:
        # If the container does not exist
        return render_template('page_no_container.html')
    elif "false" in inspect_result.stdout:
        # If the container is not running
        return render_template('page_container_stopped.html')
    
    if request.method == 'POST':
        action = request.form['action']

        if action == 'retour':
            return render_template('page_index.html')
        
        if action == 'remplissage':
            # Connexion à la base de données avec le port spécifié
            engine = create_engine('postgresql://admin:admin@localhost:5434/bdd_equide')
            Session = sessionmaker(bind=engine)
            session = Session()

            # Mapping des colonnes du CSV aux colonnes de la table
            column_mapping = {
                'Nom': 'nom_tf',
                'Sexe': 'sexe_tf',
                'Couleur': 'couleur_tf',
                'Année': 'annee_naissance_tf',
                'Parent 1': 'pere_tf',
                'Parent 2': 'mere_tf',
                'Date de décès': 'date_decee_tf',
                'Naisseur': 'naisseur_tf',
                'Lien': 'lien_ifce_tf'
            }

            # Définir les longueurs maximales pour chaque colonne
            column_max_lengths = {
                'nom_tf': 50,
                'sexe_tf': 10,
                'couleur_tf': 50,
                'pere_tf': 50,
                'mere_tf': 50,
                'naisseur_tf': 100,
                'lien_ifce_tf': 150
            }
            
            # Chemin du dossier contenant les fichiers CSV
            dossier_resultats = './resultats'

            def truncate_column_values(df, column_max_lengths):
                """Truncate column values based on the specified maximum lengths."""
                for col, max_length in column_max_lengths.items():
                    df[col] = df[col].apply(lambda x: x[:max_length] if isinstance(x, str) else x)
                return df

            def entry_exists(nom_tf, session):
                """Check if an entry with the given nom_tf already exists in the database."""
                result = session.execute(text("SELECT 1 FROM chevaux_trotteur_francais WHERE nom_tf = :nom_tf"), {'nom_tf': nom_tf}).fetchone()
                return result is not None

            def clean_nom_tf(nom_tf):
                """Clean the nom_tf by removing characters after certain patterns."""
                match = re.match(r"^[^1'\"(]+", nom_tf)
                return match.group(0).strip() if match else nom_tf.strip()

            # Parcourir tous les fichiers CSV du dossier
            for fichier in os.listdir(dossier_resultats):
                if fichier.endswith('.csv'):
                    chemin_fichier = os.path.join(dossier_resultats, fichier)
                    try:
                        # Lire le fichier CSV
                        df = pd.read_csv(chemin_fichier)
                        
                        # Renommer les colonnes selon le mapping
                        df = df.rename(columns=column_mapping)
                        
                        # Garder seulement les colonnes nécessaires pour la table
                        df = df[list(column_mapping.values())]
                        
                        # Nettoyer les noms des chevaux
                        df['nom_tf'] = df['nom_tf'].apply(clean_nom_tf)
                        
                        # Remplacer les valeurs "Non renseigné" dans la colonne 'date_decee_tf' par des valeurs NaN
                        df['date_decee_tf'] = df['date_decee_tf'].replace('Non renseigné', pd.NA)
                        
                        # Convertir la colonne 'date_decee_tf' en type datetime avec dayfirst=True
                        df['date_decee_tf'] = pd.to_datetime(df['date_decee_tf'], errors='coerce', dayfirst=True)
                        
                        # Tronquer les valeurs des colonnes selon les longueurs maximales
                        df = truncate_column_values(df, column_max_lengths)
                        
                        # Insérer les données dans la table chevaux_trotteur_francais, en vérifiant les doublons
                        for index, row in df.iterrows():
                            if not entry_exists(row['nom_tf'], session):
                                row.to_frame().T.to_sql('chevaux_trotteur_francais', engine, if_exists='append', index=False)
                        
                        # Ajouter le nom du fichier à la liste des fichiers uploadés
                        fichiers_uploades.append(fichier)
                    except Exception as e:
                        # Gérer les erreurs d'importation ici
                        print(f"Erreur lors de l'importation du fichier {fichier}: {e}")
                    finally:
                        session.close()
    
    # Rendre la page avec les fichiers uploadés
    return render_template('page_remplissage_chevaux_tf.html', fichiers_uploades=fichiers_uploades)
# |--------------------------------------------------------------------------------------------------------------------------------------------|


# |---------------------------------------------------------- PAGE REMPLISSAGES RESULTATS PMU -------------------------------------------------|
@app.route("/remplissage_tables_resultat_pmu", methods=['GET', 'POST'])
def remplissage_tables_resultat_pmu():
    # Check if the container is running
    inspect_result = subprocess.run(["docker", "inspect", "--format='{{.State.Running}}'", "container_equide"], capture_output=True, text=True)
    
    if inspect_result.returncode != 0:
        # If the container does not exist
        return render_template('page_no_container.html')
    elif "false" in inspect_result.stdout:
        # If the container is not running
        return render_template('page_container_stopped.html')
    
    message = None

    if request.method == 'POST':
        action = request.form['action']

        if action == 'retour':
            return render_template('page_index.html')
        
        if action == 'remplissage':

            #if tables_pleines():
            #    message = "Les tables doivent être purgées pour éviter les bugs."
            #else:
            #    message = call_api()
            message = call_api()

        if action == 'supprimer':
            message = delete_tables_pmu()
    
    return render_template('page_remplissage_tables_resultat_pmu.html', message=message)
# |--------------------------------------------------------------------------------------------------------------------------------------------|



# |---------------------------------------------------------- CREATION DE LA FENËTRE ----------------------------------------------------------|
def flask_thread():
    # debug=True :          donne le reload auto et les logs détaillés
    # use_reloader=True :   applique juste le reload automatique
    app.run(use_reloader=False, port=5000)

if __name__ == "__main__":
    # Créer un thread pour l'application Flask
    flask_app_thread = threading.Thread(target=flask_thread)
    flask_app_thread.start()

    # Obtenir les dimensions de l'écran principal
    screen_width = get_monitors()[0].width
    screen_height = get_monitors()[0].height

    # Calculer la largeur et la hauteur de la fenêtre en pourcentage de la taille de l'écran
    width_percent = 70  # % de la largeur de l'écran
    height_percent = 75  # % de la hauteur de l'écran

    width = int(screen_width * (width_percent / 100))
    height = int(screen_height * (height_percent / 100))

    # Créer et afficher la fenêtre PyWebView avec une taille en pourcentage de la taille de l'écran
    webview.create_window("Construction de la base de données équidé", "http://127.0.0.1:5000", width=width, height=height)

    # Attendre que la fenêtre soit complètement fermée
    webview.start()

    # Arrêter le serveur Flask une fois la fenêtre fermée
    os._exit(0)  # Utiliser os._exit() pour terminer tous les threads et le processus principal
# |-------------------------------------------------------------------------------------------------------------------------------------------|
