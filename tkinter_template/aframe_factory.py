from tkinter_template.homepage import HomeFrame
from tkinter_template.scraping_chevaux_p1 import ScrapingFrame
from tkinter_template.loading import LoadingFrame

def get_frame(frame_name, parent):
    if frame_name == 'HomeFrame':
        return HomeFrame(parent)
    elif frame_name == 'ScrapingFrame':
        return ScrapingFrame(parent)
    elif frame_name == 'LoadingFrame':
        return LoadingFrame(parent)
    else:
        raise ValueError("Unknown frame requested: " + frame_name)
