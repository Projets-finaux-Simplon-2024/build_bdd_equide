# Imports -------------------------------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import time
#----------------------------------------------------------------------------------------------------------------------------------------------------



# Configuration du pilote Selenium et ouverture du navigateur ---------------------------------------------------------------------------------------
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://infochevaux.ifce.fr/fr/info-chevaux?utm_source=Effiweb&utm_medium=Menu%20SIRE%20Demarches&utm_campaign=SIRE%20%E2%80%93%20Infochevaux'
driver.get(url)
#----------------------------------------------------------------------------------------------------------------------------------------------------


# Si on prend entre 2024 et 2015 : 637 237 chevaux
# A 100 chevaux par par page : 6372,37 (6373)

nombre_de_pages = 2  # Ajustez ce nombre selon vos besoins

# Enregistrer l'heure de début
start_time = time.time()

try:
    for i in range(nombre_de_pages):
        time.sleep(2)  # Attente pour s'assurer que la page est bien chargée

        # Extraire les informations avec Selenium
        articles = driver.find_elements(By.TAG_NAME, 'article')
        for article in articles:
            try:
                # Extraction des données de l'article
                infos_article = article.text.split('\n')
                lien_cheval = article.find_element(By.CSS_SELECTOR, 'a.strong.text-uppercase').get_attribute('href')
                nom_cheval, details = infos_article[0].split(',', 1)

                for info in infos_article:
                    # Extraction du nom, de la race, du sexe, de la couleur et de l'année
                    if ',' in info:  # Cette ligne devrait contenir les informations principales
                        details = info.split(',')
                        nom_cheval, race, sexe, couleur, annee_str = [detail.strip() for detail in details[:5]]

                # Extraction des informations sur les parents
                if info.startswith('Par'):
                    parent_info = info
                    parents = parent_info.split(' et ')

                    # Parent 1
                    parent1_details = parents[0].split(' par ')[0].strip()  # "Par NOM_DU_PARENT1 (RACE)"
                    parent1_name = ' '.join(parent1_details.split(' ')[1:])  # Exclure "Par"
                    parent1_race = parent1_details.split(' ')[-1].strip('()')  # Exclure les parenthèses

                    # Parent 2
                    parent2_details = parents[1].split(' par ')[0].strip() if len(parents) > 1 else ''
                    parent2_name = parent2_details.split(' (')[0].strip() if parent2_details else ''
                    parent2_race = parent2_details.split(' ')[-1].strip('()') if parent2_details else ''



                annee = int(annee_str)
                if annee > 2014:
                    # Afficher les résultats (ou les stocker pour une base de données)
                    print(f"Nom: {nom_cheval}, Race: {race}, Sexe: {sexe}, Couleur: {couleur}, Année: {annee}, Lien: {lien_cheval}")
                    print(f"Parent 1: {parent1_name}, Race: {parent1_race}")
                    if parent2_name and parent2_race:
                        print(f"Parent 2: {parent2_name}, Race: {parent2_race}")

            except NoSuchElementException:
                print("Un ou plusieurs éléments sont manquants dans cet article.")

        # Trouver et cliquer sur le bouton suivant
        # Remplacez 'id_du_bouton_suivant' par l'ID réel du bouton de pagination
        next_button = driver.find_element(By.ID, 'pagination')
        next_button.click()

except NoSuchElementException:
    print("Element non trouvé ou fin de la pagination.")

finally:
    driver.quit()

    # Enregistrer l'heure de fin et calculer la durée
    end_time = time.time()
    duration = end_time - start_time
    print(f"Le scraping a pris {duration} secondes.")
