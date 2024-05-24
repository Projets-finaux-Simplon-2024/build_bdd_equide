from connexions_files.con_ifce import connexion_ifce
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By    

def recup_annees():
        driver = connexion_ifce()
        try:
            wait = WebDriverWait(driver, 45)
            
            # Cliquer sur le bouton pour dérouler la liste des années si nécessaire
            toggle_button = wait.until(EC.element_to_be_clickable((By.ID, "reproducteur-annee_naissance_cheval")))
            toggle_button.click()
            
            # Attendre que la liste soit visible et récupérer les éléments LI
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[aria-labelledby='reproducteur-annee_naissance_cheval'] li")))
            li_elements = driver.find_elements(By.CSS_SELECTOR, "ul[aria-labelledby='reproducteur-annee_naissance_cheval'] li")
            
            # Extraire le texte (les années) de chaque élément LI
            years = [li.text.split()[0] for li in li_elements]  # Utiliser split() si nécessaire pour nettoyer les données
            filtered_years = [year for year in years if int(year) >= 1950]
            return filtered_years
        finally:
            driver.quit()