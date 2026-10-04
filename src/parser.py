# ============================================================
# Etape 1 : transformer une expression reguliere en arbre
#
# Exemple :  "ab|c"  donne l'arbre :
#
#            ALT
#           /   \
#       CONCAT   c
#        /  \
#       a    b
#
# Priorites (de la plus faible a la plus forte) :
#   1. l'alternative  |           -> fonction parse_alt
#   2. la concatenation ab        -> fonction parse_concat
#   3. l'etoile * (et le +)       -> dans parse_concat
#   4. lettre, point, parentheses -> fonction parse_atome
# ============================================================


class Noeud:
    """Un noeud de l'arbre.

    type   : "CHAR" (lettre), "DOT" (point), "STAR" (etoile),
             "CONCAT" (concatenation) ou "ALT" (alternative)
    valeur : la lettre, seulement pour un noeud CHAR
    gauche : premier enfant (ou None)
    droit  : deuxieme enfant (ou None)
    """
    def __init__(self, type, valeur=None, gauche=None, droit=None):
        self.type = type
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit


def afficher(n):
    """Renvoie l'arbre sous forme de texte, par exemple |(a,b)."""
    if n.type == "CHAR":
        return n.valeur
    if n.type == "DOT":
        return "."
    if n.type == "STAR":
        return "*(" + afficher(n.gauche) + ")"
    if n.type == "CONCAT":
        return "·(" + afficher(n.gauche) + "," + afficher(n.droit) + ")"
    if n.type == "ALT":
        return "|(" + afficher(n.gauche) + "," + afficher(n.droit) + ")"


class Parser:

    def __init__(self, regex):
        self.regex = regex   # l'expression a lire
        self.pos = 0         # le curseur : position du caractere courant

    def peek(self):
        """Renvoie le caractere sous le curseur, ou None si on est a la fin."""
        if self.pos < len(self.regex):
            return self.regex[self.pos]
        return None

    # ---------- Niveau 1 : l'alternative | ----------
    def parse_alt(self):
        gauche = self.parse_concat()          # premier morceau
        while self.peek() == "|":             # tant qu'il y a un |
            self.pos = self.pos + 1           # on saute le |
            droit = self.parse_concat()       # morceau suivant
            gauche = Noeud("ALT", gauche=gauche, droit=droit)
        return gauche

    # ---------- Niveau 2 et 3 : concatenation et etoile ----------
    def parse_concat(self):
        gauche = None
        # on lit des briques jusqu'a la fin, un | ou une )
        while self.peek() is not None and self.peek() != "|" and self.peek() != ")":

            element = self.parse_atome()      # une brique

            # la brique est-elle suivie d'etoiles ou de + ?
            while self.peek() == "*" or self.peek() == "+":
                if self.peek() == "*":
                    element = Noeud("STAR", gauche=element)
                else:
                    # a+ veut dire a a*
                    etoile = Noeud("STAR", gauche=element)
                    element = Noeud("CONCAT", gauche=element, droit=etoile)
                self.pos = self.pos + 1

            # on colle la brique a ce qu'on a deja construit
            if gauche is None:
                gauche = element
            else:
                gauche = Noeud("CONCAT", gauche=gauche, droit=element)

        if gauche is None:
            # rien n'a ete lu : par exemple "a|" ou "()"
            raise ValueError("Erreur : il manque une expression a la position " + str(self.pos))
        return gauche

    # ---------- Niveau 4 : une brique de base ----------
    def parse_atome(self):
        c = self.peek()

        # cas 1 : une parenthese -> on lit toute l'expression a l'interieur
        if c == "(":
            self.pos = self.pos + 1           # on saute (
            noeud = self.parse_alt()
            if self.peek() != ")":
                raise ValueError("Erreur : parenthese fermante manquante")
            self.pos = self.pos + 1           # on saute )
            return noeud

        # cas 2 : le point (n'importe quel caractere)
        if c == ".":
            self.pos = self.pos + 1
            return Noeud("DOT")

        # cas 3 : une etoile ou un + sans rien avant, par exemple "*a"
        if c == "*" or c == "+":
            raise ValueError("Erreur : " + c + " sans rien avant, a la position " + str(self.pos))

        # cas 4 : une lettre
        self.pos = self.pos + 1
        return Noeud("CHAR", valeur=c)


def parse(regex):
    """Fonction principale : prend une regex, renvoie l'arbre."""
    if regex == "":
        raise ValueError("Erreur : expression vide")
    p = Parser(regex)
    arbre = p.parse_alt()
    if p.peek() is not None:
        # il reste des caracteres non lus, par exemple "ab)"
        raise ValueError("Erreur : caractere inattendu " + p.peek())
    return arbre