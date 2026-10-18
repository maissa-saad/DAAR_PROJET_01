# ============================================================
# Etape 3 : transformer le NFA en automate deterministe (DFA)
#           par la methode des sous-ensembles
#
# Idee : un etat du DFA = un ENSEMBLE d'etats du NFA
#        (la "photo" des pions a un instant donne).
# ============================================================

from src.nfa import epsilon_fermeture, transiter


class DFA:
    """Automate deterministe.

    debut       : etat de depart (toujours 0)
    finaux      : ensemble des etats finaux
    transitions : dictionnaire (etat, lettre) -> etat cible
    lettres     : l'alphabet (lettres de la regex + "AUTRE")
    """
    def __init__(self):
        self.nb_etats = 0
        self.debut = 0
        self.finaux = set()
        self.transitions = {}
        self.lettres = set()


def alphabet(nfa):
    """Les lettres presentes sur les fleches du NFA,
    plus "AUTRE" pour tous les autres caracteres (utile pour le point)."""
    lettres = set()
    for (depart, symbole, arrivee) in nfa.transitions:
        if symbole != "EPS" and symbole != "DOT":
            lettres.add(symbole)
    lettres.add("AUTRE")
    return lettres


def construire_dfa(nfa):
    dfa = DFA()
    dfa.lettres = alphabet(nfa)

    # premiere photo : ou sont les pions avant de lire quoi que ce soit
    D0 = frozenset(epsilon_fermeture(nfa, {nfa.debut}))

    numeros = {D0: 0}          # photo -> numero d'etat dans le DFA
    dfa.nb_etats = 1
    a_traiter = [D0]

    while len(a_traiter) > 0:
        D = a_traiter.pop()

        # D est final s'il contient l'etat final du NFA
        if nfa.fin in D:
            dfa.finaux.add(numeros[D])

        for c in dfa.lettres:
            cible = frozenset(epsilon_fermeture(nfa, transiter(nfa, D, c)))

            if len(cible) == 0:
                continue                      # plus aucun pion : pas de fleche

            if cible not in numeros:          # nouvelle photo
                numeros[cible] = dfa.nb_etats
                dfa.nb_etats = dfa.nb_etats + 1
                a_traiter.append(cible)

            dfa.transitions[(numeros[D], c)] = numeros[cible]

    return dfa


def suivant(dfa, etat, c):
    """Etat atteint en lisant c depuis etat (None s'il n'y a pas de fleche)."""
    if c not in dfa.lettres:
        c = "AUTRE"
    return dfa.transitions.get((etat, c))


def accepte_dfa(dfa, mot):
    """True si le mot ENTIER est reconnu par le DFA."""
    etat = dfa.debut
    for c in mot:
        etat = suivant(dfa, etat, c)
        if etat is None:
            return False
    return etat in dfa.finaux