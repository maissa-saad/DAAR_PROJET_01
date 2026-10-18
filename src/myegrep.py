# ============================================================
# myegrep : clone simplifie de egrep
# Usage : ./myegrep <regex> <fichier>
# ============================================================

import sys
from src.parser import parse
from src.nfa import arbre_vers_nfa
from src.dfa import construire_dfa
from src.matcher import ligne_correspond
from src.minimize import minimiser
from src.kmp import kmp



def est_litteral(regex):
    """True si la regex ne contient aucun operateur (on pourra alors utiliser KMP)."""
    for c in regex:
        if c == "(" or c == ")" or c == "|" or c == "*" or c == "+" or c == ".":
            return False
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage : myegrep <regex> <fichier>", file=sys.stderr)
        sys.exit(2)

    regex = sys.argv[1]
    chemin = sys.argv[2]
    
    # 1) motif vide : erreur, comme egrep
    if regex == "":
        print("myegrep: expression vide", file=sys.stderr)
        sys.exit(2)

    # 2) choix de la methode AVANT le parsing
    if est_litteral(regex):
        # mot simple : toujours valide, pas besoin d'arbre ni d'automate
        methode = "kmp"
    else:
        # regex -> arbre (et verification de la regex)
        try:
            arbre = parse(regex)
        except ValueError as erreur:
            print(erreur, file=sys.stderr)
            sys.exit(2)
        # arbre -> NFA -> DFA -> DFA minimal
        dfa = minimiser(construire_dfa(arbre_vers_nfa(arbre)))
        methode = "automate"


    # 3) lecture du fichier ligne par ligne
    try:
        fichier = open(chemin, encoding="utf-8", errors="replace", newline="")
    except OSError as erreur:
        print(f"myegrep: {chemin}: {erreur.strerror}", file=sys.stderr)
        sys.exit(2)

    trouve = False
    with fichier:
        for ligne in fichier:
            ligne = ligne.rstrip("\n")
            if methode == "kmp":
                trouve_dans_ligne = kmp(regex, ligne)
            else:
                trouve_dans_ligne = ligne_correspond(dfa, ligne)

            if trouve_dans_ligne:
                print(ligne)
                trouve = True

    # comme egrep : code 0 si au moins une ligne trouvee, 1 sinon
    if trouve:
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()