# Imports -------------------------------------------------------------------------------------------------------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import time
import math
#----------------------------------------------------------------------------------------------------------------------------------------------------

def calcul_nb_pages(driver, annees):
    # Attendre que l'élément devienne cliquable
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".card:nth-child(1) > .card-header")))

    # Vérifier si la classe 'collapsed' est présente dans l'élément
    if "collapsed" in element.get_attribute("class"):
        # Si 'collapsed' est présent, cliquez pour déployer
        element.click()

    for i in annees:
        element = wait.until(EC.element_to_be_clickable((By.ID, "reproducteur-annee_naissance_cheval")))
        element.click()

        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, i)))
        element.click()

        time.sleep(2)

    # Attendre que le texte du h4 soit mis à jour
    nombre_chevaux_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h4.mtn.d-print-none")))

    # Extraire le texte une fois que l'élément est visible
    nombre_chevaux_str = nombre_chevaux_element.text

    # Utilisation d'une expression régulière pour extraire le nombre
    nombre = re.findall(r'\d+', nombre_chevaux_str)

    # Le résultat est une liste de chaînes de caractères contenant des nombres. 
    # Prendre le premier élément de la liste et le convertir en entier.
    nombre_chevaux = int(nombre[0]) if nombre else None

    # Calculer le nombre de pages, en arrondissant au nombre entier supérieur
    nombre_pages = math.ceil(nombre_chevaux / 100)

    return nombre_chevaux, nombre_pages