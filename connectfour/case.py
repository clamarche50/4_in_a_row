class Case:
    '''
    Classe représentant une case de la grille de jeu.

    Une case est constitutée d'un attribut Jeton, initialement None.

    Certaines fonctions y sont aussi implémentées pour permettre
    un affichage élégant de chacune des cases.

    Cette classe vous est fournie, vous n'avez pas à la modifier.
    '''

    def __init__(self):
        self.jeton = None

    def mettre_jeton(self, jeton):
        self.jeton = jeton

    def est_de_couleur(self, couleur):
        return self.jeton is not None and self.jeton.couleur == couleur

    def obtenir_couleur(self):
        return self.jeton.couleur if self.jeton else ""

    def surligner(self):
        self.jeton.surligner()

    def __str__(self):
        return str(self.jeton) if self.jeton else ' '
