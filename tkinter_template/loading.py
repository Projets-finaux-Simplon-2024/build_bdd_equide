import tkinter as tk

class LoadingFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Chargement en cours...", font=("Arial", 16))
        self.label.grid(sticky="nsew")  # Utilisez grid au lieu de pack

    def show_loading(self):
        self.label.config(text="Chargement en cours...")
        self.grid()  # Utilisez grid pour afficher le cadre

    def hide_loading(self):
        self.grid_remove()  # Utilisez grid_remove pour cacher le cadre sans le détruire
