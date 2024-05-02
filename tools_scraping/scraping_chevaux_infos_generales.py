# Imports -------------------------------------------------------------------------------------------------------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from tools_scraping.calcul_nb_pages import calcul_nb_pages
from tools_scraping.cut_article import cut_article
from connexions_files.con_ifce import connexion_ifce

import time
import pandas as pd
import os
#----------------------------------------------------------------------------------------------------------------------------------------------------



def scraping_chevaux_infos_generales(driver, nombre_pages, annees):

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

        # Chemin du dossier où stocker les fichiers
        dossier_resultats = 'resultats' 

        # Vérifiez si le dossier existe, sinon créez-le
        if not os.path.exists(dossier_resultats):
            os.makedirs(dossier_resultats)

        # Enregistrer le DataFrame dans un fichier CSV
        list_annees = '_'.join(annees)
        fichier_csv = os.path.join(dossier_resultats, f'donnees_chevaux_{list_annees}.csv')
        df.to_csv(fichier_csv, index=True)

        # Enregistrer l'heure de fin et calculer la durée
        end_time = time.time()
        duration = end_time - start_time
        
    return (duration, fichier_csv)