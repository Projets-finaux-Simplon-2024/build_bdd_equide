from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def connexion_ifce() :
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")  # Simuler une taille de fenêtre standard
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://infochevaux.ifce.fr/fr/info-chevaux?utm_source=Effiweb&utm_medium=Menu%20SIRE%20Demarches&utm_campaign=SIRE%20%E2%80%93%20Infochevaux'
    driver.get(url)
    return(driver)