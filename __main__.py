"""
Module de lancement du package connectfour. 

C'est ce module que nous allons exécuter pour démarrer votre jeu.
"""
from interface.interface_connectfour import FenetrePrincipale
from tkinter import PhotoImage

from tkinter import *
from connectfour import *
from interface import *
from PIL import ImageTk, Image


if __name__ == '__main__':

    interface = FenetrePrincipale()
    interface.tk.call('wm', 'iconphoto', interface._w, PhotoImage(file="interface\\Images\\header_logo.png"))
    interface.mainloop()
