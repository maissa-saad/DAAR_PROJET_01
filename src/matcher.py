# ============================================================
# Etape 5 : chercher le motif dans une ligne avec le DFA
#
# Une ligne correspond si, en demarrant l'automate a une
# certaine position i, on atteint un etat final.
# ============================================================

from src.dfa import suivant


def cherche_depuis(dfa, ligne, i):
    """Demarre l'automate a la position i.
    True des qu'on passe par un etat final."""
    etat = dfa.debut
    if etat in dfa.finaux:          # motif qui accepte le mot vide, ex : a*
        return True
    j = i
    while j < len(ligne):
        etat = suivant(dfa, etat, ligne[j])
        if etat is None:            # plus de fleche : echec depuis cette position
            return False
        if etat in dfa.finaux:      # motif trouve
            return True
        j = j + 1
    return False


def ligne_correspond(dfa, ligne):
    """True si le motif apparait quelque part dans la ligne."""
    for i in range(len(ligne) + 1):
        if cherche_depuis(dfa, ligne, i):
            return True
    return False