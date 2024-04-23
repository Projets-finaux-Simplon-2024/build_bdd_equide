import tkinter as tk
from tkinter_template.loading import LoadingFrame
from tkinter_template.aframe_factory import get_frame

#-------------------------------------------------------- BASE APPLICATION --------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de Scraping Equidia")
        self.setup_window()
        self.current_frame = None
        self.loading_frame = LoadingFrame(self)
        self.frames = {}  # Cache for frame instances

        self.show_frame('HomeFrame')  # Use string identifiers

    def setup_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print(screen_width, screen_height)

        window_width = int((screen_width * 80) / 100)
        window_height = int((screen_height * 80) / 100)

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def show_frame(self, frame_name):
        if self.current_frame is not None:
            self.current_frame.grid_remove()
        self.loading_frame.show_loading()  # Affiche la page de chargement
        self.after(100, lambda: self.load_frame(frame_name))  # Temporisation pour simuler un chargement

    def load_frame(self, frame_name):
        if frame_name not in self.frames:
            # Request a new frame from the factory if not cached
            self.frames[frame_name] = get_frame(frame_name, self)
        self.current_frame = self.frames[frame_name]
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.loading_frame.hide_loading()  # Cache la page de chargement après le chargement
#----------------------------------------------------------------------------------------------------------------------------------




#-------------------------------------------------------- MAIN --------------------------------------------------------------------
if __name__ == "__main__":
    print("Starting application...")
    app = App()
    print("Application is running.")
    app.mainloop()
    print("Application closed.")  # Debug: confirm application closure
#----------------------------------------------------------------------------------------------------------------------------------