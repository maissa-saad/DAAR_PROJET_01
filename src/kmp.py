# ============================================================
# Recherche d'un mot simple : algorithme de Knuth-Morris-Pratt
#
# Idee : on ne recule jamais dans le texte. En cas de difference,
# on recule seulement dans le motif, grace au tableau lps.
# ============================================================


def construire_lps(motif):
    """Tableau lps du motif.

    lps[i] = longueur du plus long debut du motif qui est aussi une fin
    de motif[0..i] (sans etre ce morceau entier).
    Exemple : "abab" donne [0, 0, 1, 2]."""
    lps = [0] * len(motif)
    longueur, i = 0, 1
    while i < len(motif):
        if motif[i] == motif[longueur]:
            longueur += 1
            lps[i] = longueur
            i += 1
        elif longueur != 0:
            longueur = lps[longueur - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp(motif, texte):
    """True si le motif apparait quelque part dans le texte."""
    if motif == "":
        return True

    lps = construire_lps(motif)
    i = 0          # position dans le texte
    j = 0          # position dans le motif
    while i < len(texte):
        if texte[i] == motif[j]:
            i += 1
            j += 1
            if j == len(motif):
                return True
        elif j != 0:
            j = lps[j - 1]        # on recule dans le motif, pas dans le texte
        else:
            i += 1
    return False