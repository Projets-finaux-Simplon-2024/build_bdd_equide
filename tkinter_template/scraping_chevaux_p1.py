import tkinter as tk
from tkinter import Button, Label, Checkbutton
import subprocess
from connexions_files.con_ifce import connexion_ifce
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#-------------------------------------------------------- SCRAPING PHASE 1 --------------------------------------------------------
class ScrapingFrame(tk.Frame):
    def __init__(self, parent):
        
        # On appelle le constructeur parent
        super().__init__(parent)

        # Pour que la grille occupe 100% de la fenêtre, il faut que tkinter
        # connaisse à l'avance le nombre de lignes et le nombre de colonnes.
        # Le paramètre weight indique que chaque colonne (et chaque ligne)
        # à le même poids. L'une ne prendra pas l'avantage sur l'autre.

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=18)
        self.grid_columnconfigure(2, weight=1)

        self.create_widgets()

        # Titre
        title_h1 = Label(self, text="Sélectionnez les années pour le scraping", font=("Arial", 16))
        title_h1.grid(row=0, column=1, columnspan=18, sticky='nsew')


        # Bouton en bas gauche
        retour = Button(self, text="Retour", command=lambda: self.master.show_frame('HomeFrame'))
        retour.grid(row=20, sticky="w")
         
        # Boutons en bas droite
        start_scrap = Button(self, text="Démarrer le Scraping", command=self.start_scraping)
        start_scrap.place(relx=0.01, rely=0.95)

        


    def create_widgets(self):

        # Récupération et affichage des années
        years = self.fetch_years_from_web()
        self.year_vars = {}
        row = 1
        col = 0

        # Placer les checkbuttons en grille, centrer en ajustant les colonnes
        for i, year in enumerate(years):
            var = tk.BooleanVar(value=False)
            self.year_vars[year] = var
            cb = Checkbutton(self, text=year, variable=var)
            cb.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 20:  # Nombre de colonnes, ajustez selon votre besoin
                col = 0
                row += 1

    def fetch_years_from_web(self):
        driver = connexion_ifce()
        try:
            wait = WebDriverWait(driver, 10)
            
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

    def start_scraping(self):
        selected_years = [year for year, var in self.year_vars.items() if var.get()]
        command = ["python.exe", "./tools_scraping/scraping_chevaux_infos_generales.py"] + selected_years
        subprocess.run(command)
#----------------------------------------------------------------------------------------------------------------------------------