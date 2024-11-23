from connectfour.jeton import Jeton
from connectfour.case import Case


class Grille:
    '''
    Classe représentant la grille de jeu de ConnectFour.

    Le système de position de la grille fonctionne comme suit:

        - La position est représentée par un tuple (colonne, ligne)

        - Le coin supérieur gauche est représenté par la positon (0, 0)

        - Le coin inférieur droit est donc représenté par la position (6, 5), 
          correspondant à (Grille.N_LIGNES - 1, Grille.N_COLONNES - 1)
    '''

    # Attributs globaux de la classe Grille.
    # Vous pouvez leur accéder avec Grille.N_LIGNES par exemple.
    N_COLONNES = 7
    N_LIGNES = 6

    def __init__(self):
        """
        Méthode spéciale initialisant une nouvelle grille.
        """
        self.cases = self.initialiser_cases_par_defaut()

        self.position_dernier_coup = None
        self.couleur_dernier_coup = None
        self.sequence_gagnante = None

    def initialiser_cases_par_defaut(self):
        '''
         Méthode initialisant le dictionaire de cases de la
        grille. Pour toutes les positions de case possibles,
        une case vide est associée comme valeur dans le dictionaire.

        Notez ici que le dictionaire est accédé par un tuple
        (colonne, ligne).

        Returns :
            Le dictionaire de cases initialisé avec des cases
            vides pour chacune des positions sur la grille
        '''
        self.cases = {}

        for i in range(0, Grille.N_COLONNES):
            for j in range(0, Grille.N_LIGNES):
                case_vide = Case()
                self.cases[(i, j)] = case_vide
        return self.cases

    def valider_coup(self, coup):
        '''
        Méthode permettant de vérifier la validité d'un coup.

        Dans le contexte du connectfour, un coup est simplement
        une colonne de la grille.

        Un coup est invalide (1) s'il n'est pas dans les limites
        ou (2) s'il est tenté sur une colonne déjà pleine. On
        retourne False ainsi qu'un message d'erreur approprié
        selon la raison de l'échec pour un coup invalide.

        Dans chacun des deux cas, la classe Grille possède les
        méthodes coup_dans_les_limites() et colonne_est_pleine(),
        utilisez les !

        Args :
            coup, entier de la colonne du coup tenté

        Returns :
            Un booléen représentant la validité du coup

            Un message d'erreur approprié si le coup est invalide, None sinon
        '''
        if not self.coup_dans_les_limites(coup):
            raise ValueError("Le coup tenté n'est pas dans les limites !")

        try:
            if self.colonne_est_pleine(coup):
                raise ValueError("Cette colonne est déjà pleine !")
        except ValueError as e:
            return e

        try:
            if coup is None:
                raise ValueError("Vous devez entrer un numéro de colonne dans la boîte de texte")
        except ValueError as e:
            return e

    def coup_dans_les_limites(self, coup):
        '''
        Vérifie si un coup est dans les limites de la grille.
        Dans notre cas, comme un coup est simplement une colonne,
        on vérifie que le coup est un entier positif et inférieur
        à Grille.N_COLONNES.

        Args :
            coup, entier de la colonne du coup

        Returns :
            True si le coup est dans les limites, faux sinon
        '''
        if Grille.N_COLONNES >= coup >= 1:
            return True
        return False

    def colonne_est_pleine(self, colonne):
        '''
        Vérifie si une colonne est pleine.

        Pour vérifier qu'une case d'une colonne est occupée,
        il suffit de valider que le jeton de la case n'est
        pas None.

        Args :
            colonne, entier de la colonne qui nous intéresse

        Returns :
            True si la colonne est pleine, False sinon
        '''
        for ligne in range(Grille.N_LIGNES):
            if self.cases[(colonne, ligne)].jeton:
                continue
            return False
        return True

    def est_pleine(self):
        '''
        Méthode qui vérifie si la grille est pleine.

        Une grille est pleine si toutes ses colonnes sont
        pleines.

        Returns :
            True si la grille est pleine, False sinon
        '''
        for i in range(0, Grille.N_COLONNES):
            for j in range(0, Grille.N_LIGNES):
                if self.cases[(i, j)].jeton:
                    continue
                return False
        return True

    def jouer_coup(self, colonne, ligne, couleur):
        '''
        Insère un jeton de la couleur "couleur" dans la colonne "colonne".

        Cette méthode doit donc:
        - Trouver la position à laquelle le jeton sera joué dans
          la colonne
        - Mettre le jeton de la bonne couleur à la position déterminée
        - Mettre à jour les attributs couleur_dernier_coup et
          position_dernier_coup

        ATTENTION: Ne dupliquez pas de code! Vous avez à
        implémenter la méthode case_est_diponible() pour vérifier
        si un jeton peut être inséré à une position.

        Une façon de procéder pour trouver la position à laquelle
        le jeton sera joué dans la colonne est de partir du
        sommet de la colonne et de descendre itérativement la
        colonne tant que la case courante est disponible. La
        position du jeton joué dans la colonne sera la position
        la plus basse de celle-ci où la case est disponible.

        Args :
            colonne, entier de la colonne où on ajoute le jeton
            couleur, string de la couleur du jeton ajouté
        '''

        self.position_dernier_coup = (colonne, ligne)
        self.cases[self.position_dernier_coup].mettre_jeton(Jeton(couleur))
        self.couleur_dernier_coup = couleur

    def case_est_disponible(self, position_case):
        '''
        Méthode vérifiant si une case est disponible pour
        l'insertion d'un jeton.

        Une certaine position est disponible si elle est contenue
        dans les clés du dictionaire de cases ET qu'il n'y a pas
        déjà un jeton à la case à cette position.

        Args :
            position_case, tuple (col, ligne) de la position tentée

        Returns :
            True si la case est disponible, False sinon
        '''
        if position_case in self.cases.keys() and not self.cases[position_case].jeton:
            return True
        return False

    def possede_un_gagnant(self):
        '''
        Méthode déterminant si la grille actuelle possède un
        gagnant.

        Pour des raisons d'efficacité de calcul, la méthode que
        nous vous demandons d'implémenter est basée sur la
        position du dernier coup.

        Le processus de validation considère les 4 directions
        possibles ([1, 1], [1, 0], [1, -1], [0, 1]) à partir de
        la position du dernier coup. Pour ce faire, on utilise
        obtenir_sequence_direction(). Si la séquence retournée
        par cette fonction est d'au moins 4 éléments, alors on la
        sauvegarde dans l'attribut sequence_gagnante.

        Cette fonction doit aussi gérer le cas où la position du
        dernier coup est à None, et retourner False.

        Returns :
            True si la grille possède un gagnant, False sinon
        '''
        if self.position_dernier_coup is None:
            return False

        directions_possibles = ([1, 1], [1, 0], [1, -1], [0, 1])

        for direction in directions_possibles:
            sequence_direction = self.obtenir_sequence_direction(self.position_dernier_coup, self.couleur_dernier_coup,
                                                                 direction)
            if len(sequence_direction) >= 4:
                self.sequence_gagnante = sequence_direction
                return True
        return False

    def obtenir_sequence_direction(self, position, couleur, direction):
        '''
        Méthode pour obtenir la séquence complète obtenue en
        partant d'une position en suivant une direction donnée.

        Ici, on fera donc appel à obtenir_sequence_vecteur() avec
        le vecteur direction et le vecteur inverse (chaque entrée
        multipliée par -1) à direction.

        La séquence totale retournée sera donc la concaténation
        de la position de départ ainsi que des deux séquences
        obtenues avec chacun des vecteurs direction.

        Args :
            position, tuple (col, ligne) de la position de départ
            couleur, string de la couleur du jeton
            direction, une liste de deux entiers représentant la
                direction de recherche

        Returns :
            Une liste représentant toutes les positions de même
            couleur suivant le vecteur direction et incluant la
            position de départ
        '''
        liste_complete = list()
        direction_inverse = list()
        x = -1 * direction[0]
        y = -1 * direction[1]

        direction_inverse.append(x)
        direction_inverse.append(y)
        liste_complete.extend(self.obtenir_sequence_vecteur(position, couleur, direction) +
                              (self.obtenir_sequence_vecteur(position, couleur, direction_inverse)))
        liste_complete.append(position)

        return liste_complete

    def obtenir_sequence_vecteur(self, position, couleur, vecteur_direction):
        '''
        Méthode retournant une liste de toutes les positions
        d'une certaine couleur à partir d'une position de départ
        en naviguant selon un vecteur de direction.

        La méthode fonctionne comme suit : on fait un pas dans la
        direction tant que la position explorée est encore dans
        la grille ET que la case contient un jeton de la couleur
        qui nous intéresse.

        N.B. Dans le cas où il n'y a aucun jeton de la bonne
                couleur dans le sens du vecteur_direction, la
                fonction devrait retourner la liste vide [].

        Args :
            position, tuple (col, ligne) de la position de départ
            couleur, string de la couleur recherchée
            vecteur_direction, liste de deux entiers représentant
                le vecteur de la direction d'exploration

        Returns :
            Une liste de tuple de positions contenant des jetons
            de la bonne couleur obtenus en partant de la position
            de départ en parcourant selon le vecteur_direction.
        '''
        liste_positions = []
        position = (position[0] + vecteur_direction[0], position[1] + vecteur_direction[1])

        while self.get_case(position):
            if self.cases[position].obtenir_couleur() == couleur:
                liste_positions.append(position)
                position = (position[0] + vecteur_direction[0], position[1] + vecteur_direction[1])
            else:
                break
        return liste_positions

    def surligner_sequence_gagnante(self):
        '''
        Cette méthode va appeler Case.surligner() sur toutes les
        cases contenues dans l'attribut sequence_gagnante.
        '''
        for case in self.sequence_gagnante:
            self.cases[case].surligner()

    def obtenir_coups_possibles(self):
        '''
        Returns :
            Une liste de toutes les colonnes non-pleines de la grille
        '''
        liste_colonnes_n_pleine = []

        for c in range(Grille.N_COLONNES):
            if not self.colonne_est_pleine(c):
                liste_colonnes_n_pleine.append(c)
        return liste_colonnes_n_pleine

    def get_case(self, position):
        '''
        Récupère une case dans la grille.

        Args :
            position, tuple (col, ligne) de la position

        Returns :
            None si la position n'est pas une clés du dictionaire
            de cases, la case correspondante sinon.
        '''
        if position not in self.cases.keys():
            return None
        else:
            return self.cases[position]

    def convertir_en_chaine(self):
        '''
        Retourne une chaîne de caractères où chaque case
        possédant un jeton est écrite sur une ligne distincte. Si
        une case ne possède pas de jeton, on n'inscrit rien pour
        cette case.

        Chaque ligne contient l'information suivante :
        colonne,ligne,couleur

        Cette méthode pourrait par la suite être réutilisée pour
        sauvegarder une grille dans un fichier.

        Returns:
            La chaîne de caractères.
        '''
        chaine_grille = ""

        for colonne in range(Grille.N_COLONNES):
            for ligne in range(Grille.N_LIGNES):
                if self.cases[(colonne, ligne)].jeton:
                    chaine_grille += f"{colonne},{ligne},{self.cases[(colonne, ligne)].jeton.couleur}\n"
                else:
                    continue
        return chaine_grille

    def charger_dune_chaine(self, chaine):
        '''
        Remplit la grille à partir d'une chaîne de caractères
        comportant l'information d'une case non-vide sur chaque ligne.

        Chaque ligne contient l'information suivante :
        colonne,ligne,couleur

        Faites donc d'abord appel à
        self.initialiser_cases_par_defaut() au début de la
        fonction et insérez un jeton aux cases contenues dans la
        chaîne.

        Args :
            chaine, string de la chaîne de caractères
            représentant le dictionaire de cases formatté
        '''
        self.initialiser_cases_par_defaut()

        for item in chaine:
            if item[4] == 'y':
                couleur = 'yellow'
            else:
                couleur = 'red'
            self.cases[(int(item[0]), int(item[2]))].mettre_jeton(Jeton(couleur))
