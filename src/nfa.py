# ============================================================
# Etape 2 : transformer l'arbre syntaxique en automate
#           non-deterministe avec epsilon-transitions (NFA)
#
# Methode de Thompson (Aho-Ullman) : on construit un petit
# automate pour chaque noeud de l'arbre, puis on les relie
# avec des epsilon-transitions.
#
# Chaque petit automate a toujours UNE entree et UNE sortie.
# ============================================================

from src.parser import parse


class NFA:
    """Automate non-deterministe.

    Les etats sont des nombres : 0, 1, 2, ...
    Une transition est un triplet (depart, symbole, arrivee).
    Symboles speciaux :
      "EPS" : epsilon-transition (on passe sans lire de caractere)
      "DOT" : n'importe quel caractere (le point de la regex)
    """
    def __init__(self):
        self.nb_etats = 0
        self.transitions = []
        self.debut = None
        self.fin = None

    def nouvel_etat(self):
        """Cree un nouvel etat et renvoie son numero."""
        etat = self.nb_etats
        self.nb_etats = self.nb_etats + 1
        return etat

    def ajouter(self, depart, symbole, arrivee):
        """Ajoute une transition."""
        self.transitions.append((depart, symbole, arrivee))


# ---------- Les gabarits de Thompson ----------

def construire_lettre(nfa, lettre):
    #   (i) --lettre--> (f)
    i = nfa.nouvel_etat()
    f = nfa.nouvel_etat()
    nfa.ajouter(i, lettre, f)
    return i, f


def construire_concat(nfa, i1, f1, i2, f2):
    #   [automate 1] --eps--> [automate 2]
    nfa.ajouter(f1, "EPS", i2)
    return i1, f2


def construire_alt(nfa, i1, f1, i2, f2):
    #         eps--> [automate 1] --eps
    #   (i)                              (f)
    #         eps--> [automate 2] --eps
    i = nfa.nouvel_etat()
    f = nfa.nouvel_etat()
    nfa.ajouter(i, "EPS", i1)
    nfa.ajouter(i, "EPS", i2)
    nfa.ajouter(f1, "EPS", f)
    nfa.ajouter(f2, "EPS", f)
    return i, f


def construire_etoile(nfa, i1, f1):
    #   (i) --eps--> [automate] --eps--> (f)
    #   + retour  f1 --eps--> i1  (recommencer)
    #   + saut    i  --eps--> f   (zero repetition)
    i = nfa.nouvel_etat()
    f = nfa.nouvel_etat()
    nfa.ajouter(i, "EPS", i1)
    nfa.ajouter(f1, "EPS", f)
    nfa.ajouter(f1, "EPS", i1)
    nfa.ajouter(i, "EPS", f)
    return i, f


# ---------- Parcours recursif de l'arbre ----------

def construire(nfa, noeud):
    """Construit l'automate du noeud et renvoie (entree, sortie)."""
    if noeud.type == "CHAR":
        return construire_lettre(nfa, noeud.valeur)

    if noeud.type == "DOT":
        return construire_lettre(nfa, "DOT")

    if noeud.type == "CONCAT":
        i1, f1 = construire(nfa, noeud.gauche)
        i2, f2 = construire(nfa, noeud.droit)
        return construire_concat(nfa, i1, f1, i2, f2)

    if noeud.type == "ALT":
        i1, f1 = construire(nfa, noeud.gauche)
        i2, f2 = construire(nfa, noeud.droit)
        return construire_alt(nfa, i1, f1, i2, f2)

    if noeud.type == "STAR":
        i1, f1 = construire(nfa, noeud.gauche)
        return construire_etoile(nfa, i1, f1)


def arbre_vers_nfa(arbre):
    """Fonction principale : arbre -> automate complet."""
    nfa = NFA()
    i, f = construire(nfa, arbre)
    nfa.debut = i
    nfa.fin = f
    return nfa


def afficher_nfa(nfa):
    """Affiche l'automate (utile pour deboguer)."""
    print("debut =", nfa.debut, " fin =", nfa.fin)
    for (depart, symbole, arrivee) in nfa.transitions:
        print("  ", depart, "--" + symbole + "-->", arrivee)