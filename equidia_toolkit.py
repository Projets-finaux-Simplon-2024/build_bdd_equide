# |---------------------------------------------------------- IMPORTS -------------------------------------------------------------------------|
# Libs
import webview
from screeninfo import get_monitors
from flask import Flask, render_template, request

# Outils
import threading
import os

# Local
from tools_scraping.recup_annees import recup_annees
from tools_scraping.calcul_nb_pages import calcul_nb_pages
from connexions_files.con_ifce import connexion_ifce
from tools_scraping.scraping_chevaux_infos_generales import scraping_chevaux_infos_generales

# |--------------------------------------------------------------------------------------------------------------------------------------------|

app = Flask(__name__)

# Initialisation de la variable globale
list_annees = None

# |---------------------------------------------------------- PAGE ACCUEIL --------------------------------------------------------------------|
@app.route("/")
def index():
    return render_template('page_index.html')
# |--------------------------------------------------------------------------------------------------------------------------------------------|






# |---------------------------------------------------------- PAGE DE SCRAPING DE BASE --------------------------------------------------------|
@app.route("/scraping_chevaux_bases", methods=['GET', 'POST'])
def scraping_chevaux_bases():
    global list_annees

    if not list_annees:
        list_annees = recup_annees()

    context = {
        'list_annees': list_annees
    }

    if request.method == 'POST':
        action = request.form['action']

        # Récupérer les années sélectionnées dans le formulaire
        annees = request.form.getlist('annees[]')

        driver = connexion_ifce()

        # Appeler la fonction pour obtenir les informations supplémentaires
        nombre_chevaux, nombre_pages = calcul_nb_pages(driver, annees)

        # Temps de scraping par page en secondes
        temps_par_page = 5.5

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
        print(f"Temps total estimé pour le scraping (pour 5.5s par page de 100 articles): {heures} heures {minutes} minutes {secondes} secondes")
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

            duration, fichier_csv = scraping_chevaux_infos_generales(driver, nombre_pages, annees)

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

            return render_template('page_scraping_chevaux_bases.html', **context)

    return render_template('page_scraping_chevaux_bases.html', **context)
# |--------------------------------------------------------------------------------------------------------------------------------------------|






# |---------------------------------------------------------- CREATION DE LA FENËTRE ----------------------------------------------------------|
def flask_thread():
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
    height_percent = 70  # % de la hauteur de l'écran

    width = int(screen_width * (width_percent / 100))
    height = int(screen_height * (height_percent / 100))

    # Créer et afficher la fenêtre PyWebView avec une taille en pourcentage de la taille de l'écran
    webview.create_window("Construction de la base de données équidé", "http://127.0.0.1:5000", width=width, height=height)

    # Attendre que la fenêtre soit complètement fermée
    webview.start()

    # Arrêter le serveur Flask une fois la fenêtre fermée
    os._exit(0)  # Utiliser os._exit() pour terminer tous les threads et le processus principal
# |-------------------------------------------------------------------------------------------------------------------------------------------|
