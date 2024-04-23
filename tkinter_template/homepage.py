import tkinter as tk
from tkinter import ttk


#-------------------------------------------------------- ACCUEIL -----------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ttk.Label(self, text="Bienvenue dans l'Application de Scraping Equidia")
        label.pack(pady=10)

        # Utilisez le nom du cadre en chaîne pour la commande du bouton
        start_button = ttk.Button(self, text="Commencer le Scraping", command=lambda: parent.show_frame('ScrapingFrame'))
        start_button.pack(pady=20)

#----------------------------------------------------------------------------------------------------------------------------------