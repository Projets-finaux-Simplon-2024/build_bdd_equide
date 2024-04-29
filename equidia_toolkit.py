from flask import Flask, render_template
import webview
import threading
import os

app = Flask(__name__)


# |---------------------------------------------------------- PAGE ACCUEIL --------------------------------------------------------------------|
@app.route("/")
def index():
    # Notez le chemin mis à jour pour inclure le sous-dossier
    return render_template('index.html')
# |--------------------------------------------------------------------------------------------------------------------------------------------|






# |---------------------------------------------------------- PAGE DE SCRAPING DE BASE --------------------------------------------------------|
@app.route("/second-page")
def second_page():
    # De même, mettez à jour le chemin ici
    return render_template('scraping_chevaux_bases.html')
# |--------------------------------------------------------------------------------------------------------------------------------------------|






# |---------------------------------------------------------- CREATION DE LA FENËTRE ----------------------------------------------------------|
def flask_thread():
    app.run(use_reloader=False, port=5000)

if __name__ == "__main__":
    # Créer un thread pour l'application Flask
    flask_app_thread = threading.Thread(target=flask_thread)
    flask_app_thread.start()

    # Créer et afficher la fenêtre PyWebView
    webview.create_window("Mon Application Flask", "http://127.0.0.1:5000")

    # Attendre que la fenêtre soit complètement fermée
    webview.start()

    # Arrêter le serveur Flask une fois la fenêtre fermée
    os._exit(0)  # Utiliser os._exit() pour terminer tous les threads et le processus principal
# |-------------------------------------------------------------------------------------------------------------------------------------------|
