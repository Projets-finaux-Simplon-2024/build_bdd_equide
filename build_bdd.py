# Imports -------------------------------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from calcul_nb_pages import calcul_nb_pages
from cut_article import cut_article

import time
import pandas as pd
import sys
#----------------------------------------------------------------------------------------------------------------------------------------------------





# Configuration du pilote Selenium et ouverture du navigateur ---------------------------------------------------------------------------------------
# Configurer les options Chrome pour le mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")  # Simuler une taille de fenêtre standard
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
url = 'https://infochevaux.ifce.fr/fr/info-chevaux?utm_source=Effiweb&utm_medium=Menu%20SIRE%20Demarches&utm_campaign=SIRE%20%E2%80%93%20Infochevaux'
driver.get(url)
#----------------------------------------------------------------------------------------------------------------------------------------------------






# Calcul du nombre de pages a scraper ---------------------------------------------------------------------------------------------------------------
# Récupérer les arguments de la ligne de commande (à l'exception du nom du script)
arguments = sys.argv[1:]

# Définit une année par défaut si aucun argument n'est passé
if not arguments:
    annees = ['2024']
else:
    annees = arguments

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
#----------------------------------------------------------------------------------------------------------------------------------------------------







print('---------------------------------------------------Démarrage du scraping---------------------------------------------------------\n')
# Enregistrer l'heure de début
start_time = time.time()
wait = WebDriverWait(driver, 10)

# Mise à disposition de 100 réponses par page
element = wait.until(EC.element_to_be_clickable((By.ID, "resultatParPage")))
element.click()

dropdown = driver.find_element(By.ID, "resultatParPage")
dropdown.find_element(By.XPATH, "//option[. = '100']").click()

# Initialisation du DataFrame
print('Initialisation du dataframe...\n')
e=0
columns = ['Nom', 'Race', 'Sexe', 'Couleur', 'Année', 'Parent 1', 'Race Parent 1', 'Parent 2', 'Race Parent 2', 'Date de décès', 'Naisseur', 'Lien']
df = pd.DataFrame(columns=columns)

try:
    for i in range(nombre_pages):
        time.sleep(2)  # Attente pour s'assurer que la page est bien chargée

        # Extraire les informations avec Selenium
        articles = driver.find_elements(By.TAG_NAME, 'article')

        for article in articles:
            e = e+1
            nom_cheval, race, sexe, couleur, annee_str, parent1_name, parent1_race, parent2_name, parent2_race, date_deces, naisseur, lien_cheval = cut_article(article)
            print(f"{e} Nom: {nom_cheval} | Race: {race} | Sexe: {sexe} | Couleur: {couleur} | Année: {annee_str} | Parent1: {parent1_name} | Parent2: {parent2_name} | Décès: {date_deces}, Naisseur: {naisseur}")

            new_row = pd.DataFrame([{'Nom': nom_cheval, 'Race': race, 'Sexe': sexe, 'Couleur': couleur, 'Année': annee_str, 'Parent 1': parent1_name, 'Race Parent 1': parent1_race, 'Parent 2': parent2_name, 'Race Parent 2': parent2_race, 'Date de décès': date_deces, 'Naisseur': naisseur, 'Lien': lien_cheval}])
            df = pd.concat([df, new_row], ignore_index=True)

        try:
            # Localiser le bouton 'Suivant'
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.page-item.next:not(.disabled) a')
            
            # Cliquer sur le bouton 'Suivant' s'il est trouvé
            next_button.click()
        except NoSuchElementException:
            # Si le bouton 'Suivant' n'est pas trouvé, cela pourrait signifier la fin de la pagination
            print("\nFin de la pagination atteinte car bouton 'Suivant' non trouvé.\n")
            break

        # Attendre un peu pour que la page suivante se charge
        time.sleep(2)

except NoSuchElementException:
    print(f"Une erreur est survenue lors de la navigation : {e}\n")

finally:
    driver.quit()

    # Afficher le DataFrame
    # print(df)

    # Enregistrer le DataFrame dans un fichier CSV
    list_annees = '_'.join(annees)
    fichier_csv = f'donnees_chevaux_{list_annees}.csv'
    df.to_csv(fichier_csv, index=True)

    # Afficher un message pour confirmer l'enregistrement
    print(f"Les données ont été enregistrées dans le fichier '{fichier_csv}'.\n")

    # Enregistrer l'heure de fin et calculer la durée
    end_time = time.time()
    duration = end_time - start_time

    # Convertir le temps total en heures, minutes et secondes
    heures_duration = duration // 3600
    minutes_duration = (duration % 3600) // 60
    secondes_duration = duration % 60

    print(f"Le scraping a pris {heures} heures {minutes} minutes {secondes} secondes.\n")
