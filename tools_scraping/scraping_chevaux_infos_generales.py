# Imports -------------------------------------------------------------------------------------------------------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert

from tools_scraping.cut_article import cut_article

import time
import pandas as pd
import os
#----------------------------------------------------------------------------------------------------------------------------------------------------


def wait_for_page_load_and_overlay_disappear(driver, timeout=45):
    # Wait for the document to be fully loaded
    WebDriverWait(driver, timeout).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    
    handle_alert(driver)

    # Wait for the loading overlay to disappear
    WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'loadingoverlay')))

def handle_alert(driver):
    try:
        alert = Alert(driver)
        print(f"Alert text: {alert.text}")
        alert.accept()  # ou alert.dismiss() si vous voulez fermer l'alerte sans accepter
    except NoAlertPresentException:
        pass


def scraping_chevaux_infos_generales(driver, nombre_pages, annees):

    print('---------------------------------------------------Démarrage du scraping---------------------------------------------------------\n')
    # Enregistrer l'heure de début
    start_time = time.time()
    wait = WebDriverWait(driver, 45)

    wait_for_page_load_and_overlay_disappear(driver)

    # Mise à disposition de 100 réponses par page
    element = wait.until(EC.element_to_be_clickable((By.ID, "resultatParPage")))
    element.click()

    dropdown = driver.find_element(By.ID, "resultatParPage")
    dropdown.find_element(By.XPATH, "//option[. = '100']").click()

    # Initialisation du DataFrame
    print('Initialisation du dataframe...\n')
    e=0
    columns = ['Nom', 'Race', 'Sexe', 'Couleur', 'Année', 'Parent 1', 'Parent 2', 'Date de décès', 'Naisseur', 'Lien']
    df = pd.DataFrame(columns=columns)
    pagination = 1

    try:
        for i in range(nombre_pages):
            # Assurer que la page est complètement chargée et que le loading overlay est absent
            wait_for_page_load_and_overlay_disappear(driver)
            
            # Extraire les informations avec Selenium
            articles = driver.find_elements(By.TAG_NAME, 'article')

            for article in articles:
                nom_cheval, race, sexe, couleur, annee_str, parent1_name, parent2_name, date_deces, naisseur, lien_cheval = cut_article(article)
                if race == 'Trotteur Francais':
                    e = e+1
                    print(f"{e} Nom: {nom_cheval} | Race: {race} | Sexe: {sexe} | Couleur: {couleur} | Année: {annee_str} | Parent1: {parent1_name} | Parent2: {parent2_name} | Décès: {date_deces}, Naisseur: {naisseur}, Page: {pagination}")

                    new_row = pd.DataFrame([{'Nom': nom_cheval, 'Race': race, 'Sexe': sexe, 'Couleur': couleur, 'Année': annee_str, 'Parent 1': parent1_name, 'Parent 2': parent2_name, 'Date de décès': date_deces, 'Naisseur': naisseur, 'Lien': lien_cheval}])
                    df = pd.concat([df, new_row], ignore_index=True)


            try:
                    wait_for_page_load_and_overlay_disappear(driver)


                    # Localiser le bouton 'Suivant'
                    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.page-item.next:not(.disabled) a')))

                    # Cliquer sur le bouton 'Suivant' s'il est trouvé
                    next_button.click()

                    # Augmenter le numéro de page
                    pagination += 1

                    # Assurer que la nouvelle page est complètement chargée et que le loading overlay est absent
                    wait_for_page_load_and_overlay_disappear(driver)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'article')))

            except TimeoutException:
                print("\nFin de la pagination atteinte ou le bouton 'Suivant' n'est pas cliquable.\n")
                break

    except NoSuchElementException as ex:
        print(f"Une erreur est survenue lors de la navigation : {ex}\n")
    except TimeoutException as ex:
        print(f"TimeoutException: {ex}\n")

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
        
    return (e, duration, fichier_csv)