from tkinter import messagebox, filedialog
import tkinter as tk
from tkinter import *
from connectfour.partie import PartieConnectFour
from connectfour.exceptions import *
from PIL import ImageTk, Image

# Variables globales
N_COLONNES = 7
N_LIGNES = 6


class FenetrePrincipale(Tk):
    """
    Classe principal qui définit la fenêtre de jeu ainsi que les différents widgets
    présents sur cette fenêtre.
    """
    def __init__(self):
        super().__init__()
        self.partie = PartieConnectFour()
        self.exc = ExceptionConnect4()
        self.geometry("630x725+600+150")
        self.resizable(False, False)
        self.canvas_jeu = CanvasConnect4(self)
        self.canvas_jeu.grid()
        self.title("4 in a row")
        self.image = Image.open('interface\\Images\\logo_c4.png')
        self.photo = ImageTk.PhotoImage(self.image)

        self.photo_label = Label(image=self.photo)
        self.photo_label.image = self.photo
        self.photo_label.grid(row=1, column=0, sticky=W, padx=15, pady=5)

        self.frame_jouer = LabelFrame(self, borderwidth=5, height=200, relief=RIDGE, text="Jouer sur la grille",
                                      font=("Arial Bold", 11), pady=6)
        self.frame_jouer.grid(row=1, column=0, pady=25, sticky=S)

        self.joueur = Label(self.frame_jouer, text="Joueur 1")
        self.joueur.grid()

        self.demande_no = Label(self.frame_jouer, text="Veuillez entrer un numero de colonne")
        self.demande_no.grid(padx=8)

        self.entree = Entry(self.frame_jouer)
        self.entree.grid(padx=4, pady=4)
        self.entree.bind("<Return>", self.capturer_entree)

        self.text_valider = Label(self.frame_jouer, text="", foreground="red")
        self.text_valider.grid()

        self.frame_options = LabelFrame(self, borderwidth=5, relief=RIDGE, text="Options de partie",
                                        font=("Arial Bold", 11), pady=4)
        self.frame_options.grid(row=1, column=0, sticky=E+S, padx=20, pady=25)

        self.bouton_reset = HoverButton(self.frame_options, text="Reinitialiser la partie", activebackground="blue",
                                        activeforeground="white", command=self.reinitialiser_partie)
        self.bouton_reset.grid(padx=8, pady=3, sticky=W+E)

        self.bouton_sauvegarde = HoverButton(self.frame_options, text="Sauvegarder la partie", activebackground="blue",
                                             activeforeground="white", command=self.sauvegarder_partie)
        self.bouton_sauvegarde.grid(padx=8, pady=3, sticky=W+E)

        self.bouton_charger = HoverButton(self.frame_options, text="Charger une partie", activebackground="blue",
                                          activeforeground="white", command=self.charger_fichier)
        self.bouton_charger.grid(padx=8, pady=3, sticky=W+E)

    def capturer_entree(self, event):
        '''
        La fonction de callback pour l'entrée de la colonne par l'utilisateur.
        La boîte de texte self.entree capture le chiffre de la colonne et appelle cet fonction.
        Cette fonction va aussi gérer les exceptions en cas d'erreur de frappe par
        l'utilisateur tel qu'un nombre invalide ou une entrée vide.

        Args:
            event: int représentant le numéro de la colonne joué par l'utilisateur.
        '''
        coup_tente = self.entree.get()
        self.text_valider.config(text="")
        try:
            if coup_tente == "":
                raise ExceptionVide

            if not int(coup_tente):
                raise ValueError

            else:
                self.coup_valide(int(coup_tente))

        except ExceptionVide:
            self.text_valider["text"] = "Vous devez entrer un chiffre entre 1 et 7."
            self.text_valider.after(0, lambda: self.entree.delete(0, "end"))
        except ValueError:
            self.text_valider["text"] = "Seulement les valeurs numériques sont acceptées !"
            self.text_valider.after(0, lambda: self.entree.delete(0, "end"))

    def obtenir_case(self, couleur):
        '''
        Méthode qui détermine la position à laquelle un jeton est joué .
        Après que le coup est joué, la boîte de texte pour entrer
        un numéro de colonne est effacé automatiquement. Puis, la fonction fait appel
        à la méthode partie_terminee() du module Partie pour vérifier l'état de la partie.
        Dans le cas d'un gagnant détecté, on fait appel à fin_partie().
        Args:
            couleur: string de la couleur du jeton joué.

        Returns:

        '''
        colonne = int(self.entree.get())-1
        ligne = self.obtenir_ligne(colonne)

        position_coup = self.canvas_jeu.jeton[colonne, ligne]
        self.canvas_jeu.itemconfig(position_coup, fill=couleur)
        self.entree.delete(0, "end")

        self.partie.grille.jouer_coup(colonne, ligne, couleur)
        if not self.partie.partie_terminee():
            self.changement_joueur()
        else:
            self.fin_partie()

    def changement_joueur(self):
        '''
        Méthode qui fait appel à changer_joueur() du module Partie afin de changer
        les attributs du module après chaque coup.
        '''
        self.partie.changer_joueur()

    def obtenir_ligne(self, colonne):
        '''
        Cette méthode va trouver la première case vide en procédant par itération
        depuis le bas de la colonne tentée.
        Args:
            colonne: int de la colonne tentée par l'utilisateur.

        Returns: int du numéro de la première ligne disponible.

        '''
        for i in range(N_LIGNES-1, -1, -1):
            position_coup = self.canvas_jeu.jeton[colonne, i]
            if self.canvas_jeu.itemcget(position_coup, "fill") == "black":
                return i

    def obtenir_couleur(self):
        '''
        Méthode qui va obtenir la couleur du jeton a joué en fonction du
        joueur courant. Ensuite, un appel pour obtenir la case est effectuée.
        Returns:

        '''
        joueur_courant = self.joueur.cget("text")

        if joueur_courant == "Joueur 1":
            couleur = "yellow"
            self.joueur["text"] = "Joueur 2"
        else:
            couleur = "red"
            self.joueur["text"] = "Joueur 1"

        self.obtenir_case(couleur)

    def coup_valide(self, colonne):
        '''
        Méthode qui va gérer les exceptions liées à la grille de jeu, c'est-à-dire
        les coups dans les limites et les colonnes pleines.
        Args:
            colonne: int de la colonne tentée.

        Returns:

        '''
        try:
            if not self.partie.grille.coup_dans_les_limites(colonne):
                raise ExceptionLimite("Le coup tenté n'est pas dans les limites !")

            elif self.partie.grille.colonne_est_pleine(colonne - 1):
                raise ExceptionColonne("Le coup est tenté dans une colonne déjà pleine !")

            else:
                self.obtenir_couleur()

        except (ExceptionLimite, ExceptionColonne) as e:
            affichage = e.message
            self.text_valider["text"] = affichage
            self.text_valider.after(0, lambda: self.entree.delete(0, "end"))

    def reinitialiser_partie(self):
        '''
        Méthode pour réinitialiser une partie à tout moment lorsque désiré. Un bouton
        est lié à cette méthode pour en faire l'appel. Permet de réinitialiser les
        cases du module grille.py et les attributs de partie.py également.
        Returns:

        '''
        self.canvas_jeu.creer_jeton()
        self.partie = PartieConnectFour()
        self.joueur["text"] = "Joueur 1"
        self.demande_no["text"] = "Veuillez entrer un numero de colonne"
        self.text_valider["text"] = ""

    def fin_partie(self):
        '''
        Méthode qui gère la fin d'une partie en affichant une boîte de dialogue appropriée
        et effectue les commandes en fonction de l'utilisateur.
        Returns:

        '''
        if self.partie.gagnant_partie:

            for i in self.partie.grille.sequence_gagnante:
                jeton_gagnant = self.canvas_jeu.jeton[i]
                self.canvas_jeu.itemconfig(jeton_gagnant, fill="green")

            msg_box = messagebox.askyesno(title="Gagnant de la partie !", message=f"Félicitation au "
                                          f"{self.partie.gagnant_partie} pour avoir gagné la partie !\n"
                                          f"Désirez-vous jouer une autre partie ?")
            if not msg_box:
                self.destroy()
            else:
                self.reinitialiser_partie()

        if self.partie.partie_nulle:
            msg_box = messagebox.askyesno(title='Match nul', message="C'est un match nul !\n"
                                          "Désirez-vous jouer une autre partie ?")
            if not msg_box:
                self.destroy()
            else:
                self.reinitialiser_partie()

    def charger_fichier(self):
        '''
        Méthode pour charger une partie à partir d'un fichier .txt.
        Returns:

        '''
        game_file = filedialog.askopenfilename(title="Choisissez un fichier .txt", filetypes=[("Text files", "*.txt")])
        self.partie = PartieConnectFour(game_file)

        with open(game_file, 'r') as f:
            attributs_partie = [next(f).strip('\n') for ligne in range(3)]
            charger_partie = f.readlines()

        if attributs_partie[0] == 'yellow':
            self.joueur["text"] = "Joueur 1"
        else:
            self.joueur["text"] = "Joueur 2"

        self.canvas_jeu.itemconfig("oval", fill="black")

        for ligne in charger_partie:
            if ligne[4] == 'y':
                color = 'yellow'
            else:
                color = 'red'
            case_a_charge = self.canvas_jeu.jeton[int(ligne[0]), int(ligne[2])]
            self.canvas_jeu.itemconfig(case_a_charge, fill=color)

    def sauvegarder_partie(self):
        '''
        Méthode pour permettre la sauvegarde d'une partie dans un fichier .txt.
        Returns:

        '''
        try:
            file_save = filedialog.asksaveasfilename(title="Sauvegardez la partie", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            self.partie.sauvegarder(file_save)

        except FileNotFoundError:
            self.text_valider["text"] = "Aucun fichier n'a été sauvegardé !"
            self.text_valider.after(0, lambda: self.entree.delete(0, "end"))


class CanvasConnect4(Canvas):
    '''
    La classe du canevas qui va créer les cases bleues de la grille de jeu ainsi que
    les ronds vides qui contiendront les jetons.
    '''
    def __init__(self, parent, nb_pixels_par_case=90):
        super().__init__(master=parent, width=7*nb_pixels_par_case,
                         height=6*nb_pixels_par_case+20, borderwidth=0,
                         highlightthickness=0)
        self.nb_pixels_par_case = nb_pixels_par_case
        self.jeton = {}
        self.creer_grille()
        self.creer_jeton()

    def creer_grille(self):

        for colonne in range(N_COLONNES):
            for ligne in range(N_LIGNES):
                x1 = colonne * self.nb_pixels_par_case
                y1 = ligne * self.nb_pixels_par_case
                x2 = x1 + self.nb_pixels_par_case
                y2 = y1 + self.nb_pixels_par_case
                self.create_rectangle(x1, y1, x2, y2, fill="blue", tags="rect")
        self.create_line(631, 0, 631, 540, fill="black")

        for i in range(1, 8):
            self.create_text((45+90*(i-1)), 552, text=str(i), font=("Arial Bold", 18))

    def creer_jeton(self):

        for colonne in range(N_COLONNES):
            for ligne in range(N_LIGNES):
                x1 = colonne * self.nb_pixels_par_case
                y1 = ligne * self.nb_pixels_par_case
                x2 = x1 + self.nb_pixels_par_case
                y2 = y1 + self.nb_pixels_par_case
                self.jeton[colonne, ligne] = self.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black", tags="oval")


class HoverButton(tk.Button):
    '''
    Une classe créée pour afficher des boutons personnalisés qui change de couleur
    lorsque la souris navigue au-dessus. Cette classe de boutons hérite du tk.Button
    et ajoute une touche de beauté. Utilisé pour les boutons du cadre 'Options de partie'
    '''
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']
        self['foreground'] = self['activeforeground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground
