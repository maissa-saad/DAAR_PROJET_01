def est_concat_simple(regex):
    """
    Vérifie si une expression régulière est uniquement
    une suite de lettres ASCII.

    Retourne :
        True  -> si la regex peut être traitée par KMP
        False -> si elle contient un autre élément
    """

    if regex == "":
        return False

    for caractere in regex:
        if not (('a' <= caractere <= 'z') or
                ('A' <= caractere <= 'Z')):
            return False

    return True
