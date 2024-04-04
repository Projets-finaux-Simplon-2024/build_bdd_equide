from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://infochevaux.ifce.fr/fr/info-chevaux?utm_source=Effiweb&utm_medium=Menu%20SIRE%20Demarches&utm_campaign=SIRE%20%E2%80%93%20Infochevaux'
driver.get(url)

annee = ['2023', '2024']

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
nombre_chevaux_text = nombre_chevaux_element.text

# Afficher le contenu extrait
print(nombre_chevaux_text)

driver.quit()