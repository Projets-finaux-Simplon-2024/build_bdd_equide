from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import math

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://infochevaux.ifce.fr/fr/info-chevaux?utm_source=Effiweb&utm_medium=Menu%20SIRE%20Demarches&utm_campaign=SIRE%20%E2%80%93%20Infochevaux'
driver.get(url)

annee = ['2023', '2024', '2022']

# Attendre que le bouton soit cliquable et cliquer dessus
driver.set_window_size(1936, 1048)

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".card:nth-child(1) > .card-header")))
element.click()
for i in annee:
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, "reproducteur-annee_naissance_cheval")))
    element.click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, i)))
    element.click()

    time.sleep(2)

# Attendre que le texte du h4 soit mis à jour
wait = WebDriverWait(driver, 10)
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

# Temps de scraping par page en secondes
temps_par_page = 3

# Calculer le temps total en secondes
temps_total_secondes = nombre_pages * temps_par_page

# Convertir le temps total en heures, minutes et secondes
heures = temps_total_secondes // 3600
minutes = (temps_total_secondes % 3600) // 60
secondes = temps_total_secondes % 60

# Afficher les résultats
print(f"Nombre de chevaux : {nombre_chevaux}")
print(f"Nombre de pages : {nombre_pages}")
print(f"Temps total estimé pour le scraping (pour 3s par page): {heures} heures {minutes} minutes {secondes} secondes")

# Fermer le navigateur
driver.quit()