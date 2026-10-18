def construire_lps(motif):
    """
    Construit le tableau LPS du motif.

    LPS[i] indique la longueur du plus long
    préfixe propre de motif[0:i+1] qui est
    également un suffixe.
    """

    lps = [0] * len(motif)

    longueur = 0
    i = 1

    while i < len(motif):

        if motif[i] == motif[longueur]:
            longueur += 1
            lps[i] = longueur
            i += 1

        else:
            if longueur != 0:
                longueur = lps[longueur - 1]
            else:
                lps[i] = 0
                i += 1

    return lps



def kmp(motif, texte):
    """
    Recherche motif dans texte avec l'algorithme KMP.

    Retourne True si motif apparaît dans texte,
    False sinon.
    """

    if motif == "":
        return True

    lps = construire_lps(motif)

    i = 0
    j = 0

    while i < len(texte):

        if texte[i] == motif[j]:
            i += 1
            j += 1

            if j == len(motif):
                return True

        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False



