from connectfour.grille import Grille
from connectfour.joueur import JoueurHumain


class FichierIntrouvable(Exception):
    pass


class PartieConnectFour:
    def __init__(self, nom_fichier=None):
        '''
        Méthode d'initialisation d'une partie.
        '''
        self.grille = Grille()

        self.gagnant_partie = None
        self.partie_nulle = False

        if nom_fichier is not None:
            self.charger(nom_fichier)
        else:
            self.initialiser_joueurs()

    def initialiser_joueurs(self):
        '''
        On initialise ici quatre attributs : joueur_jaune,
        joueur_rouge, joueur_courant et couleur_joueur_courant.

        joueur_courant est initialisé par défaut au joueur_jaune
        et couleur_joueur_courant est initialisée à "jaune".

        Pour créer les objets joueur, faites appel à creer_joueur()
        '''
        self.joueur1 = JoueurHumain("yellow")
        self.joueur2 = JoueurHumain("red")
        self.joueur_courant = self.joueur1
        self.couleur_joueur_courant = "yellow"

    def partie_terminee(self):
        '''
        Méthode vérifiant si la partie est terminée.

        Si la grille est pleine, on ajuste l'attribut
        partie_nulle à True.

        Si la grille possède un gagnant, on assigne la couleur du
        joueur courant à l'attribut gagnant_partie.

        Returns :
            True si la partie est terminée, False sinon
        '''
        if self.grille.est_pleine():
            self.partie_nulle = True
            return True
        elif self.grille.possede_un_gagnant():
            if self.joueur_courant.couleur == "yellow":
                self.gagnant_partie = "Joueur 1"
            else:
                self.gagnant_partie = "Joueur 2"
            return True
        else:
            return False

    def changer_joueur(self):
        '''
        En fonction de la couleur du joueur courant actuel, met à
        jour les attributs joueur_courant et couleur_joueur_courant.
        '''
        if self.joueur_courant is self.joueur1:
            self.couleur_joueur_courant = "red"
            self.joueur_courant = self.joueur2
        else:
            self.couleur_joueur_courant = "yellow"
            self.joueur_courant = self.joueur1

    def sauvegarder(self, nom_fichier):
        '''
        Sauvegarde une partie dans un fichier. Le fichier
        contiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant le type du joueur jaune.
        - Une ligne contenant le type du joueur rouge.
        - Le reste des lignes correspondant à la grille. Voir la
          méthode convertir_en_chaine de la grille pour le
          format.

        Args :
            nom_fichier, le string du nom du fichier où sauvegarder.
        '''
        with open(nom_fichier, "w") as fichier_sauvegarde:
                fichier_sauvegarde.write(f"{self.couleur_joueur_courant}\nHumain\nHumain\n")
                fichier_sauvegarde.write(self.grille.convertir_en_chaine())

    def charger(self, nom_fichier):
        '''
        Charge une partie dans à partir d'un fichier. Le fichier
        a le même format que la méthode de sauvegarde.

        Args:
            nom_fichier: Le string du nom du fichier à charger.
        '''

        with open(nom_fichier, "r") as fichier_sauvegarde:
            attributs_partie = [next(fichier_sauvegarde).strip('\n') for i in range(3)]
            attributs_grille = fichier_sauvegarde.readlines()

        self.joueur1 = JoueurHumain("yellow")
        self.joueur2 = JoueurHumain("red")
        self.couleur_joueur_courant = attributs_partie[0]

        if self.couleur_joueur_courant == "yellow":
            self.joueur_courant = self.joueur1
        else:
            self.joueur_courant = self.joueur2

        self.grille.charger_dune_chaine(attributs_grille)

