# ============================================================
# Etape 4 : minimiser le DFA (algorithme de Moore)
#
# Idee : on part de 2 groupes (finaux / non finaux), puis on
# decoupe les groupes tant que des etats d'un meme groupe ne
# vont pas vers les memes groupes.
# A la fin, chaque groupe devient UN etat du DFA minimal.
# ============================================================

from src.dfa import DFA


def minimiser(dfa):
    lettres = sorted(dfa.lettres)     # toujours le meme ordre

    # 1) depart : finaux -> groupe 0, non finaux -> groupe 1
    groupe = {}
    for e in range(dfa.nb_etats):
        if e in dfa.finaux:
            groupe[e] = 0
        else:
            groupe[e] = 1
    nb_groupes = len(set(groupe.values()))

    # 2) on decoupe jusqu'a ce que ce soit stable
    while True:
        signatures = {}               # signature -> numero du nouveau groupe
        nouveau_groupe = {}

        for e in range(dfa.nb_etats):
            # signature = mon groupe + le groupe ou mene chaque lettre
            sig = [groupe[e]]
            for c in lettres:
                cible = dfa.transitions.get((e, c))
                if cible is None:
                    sig.append(None)              # pas de fleche
                else:
                    sig.append(groupe[cible])
            sig = tuple(sig)                      # une liste ne peut pas etre une cle

            if sig not in signatures:
                signatures[sig] = len(signatures) # nouveau groupe
            nouveau_groupe[e] = signatures[sig]

        groupe = nouveau_groupe
        if len(signatures) == nb_groupes:         # plus aucun decoupage : stable
            break
        nb_groupes = len(signatures)

    # 3) construire le DFA minimal : un etat par groupe
    mini = DFA()
    mini.lettres = dfa.lettres
    mini.nb_etats = nb_groupes
    mini.debut = groupe[dfa.debut]
    for e in range(dfa.nb_etats):
        if e in dfa.finaux:
            mini.finaux.add(groupe[e])
        for c in lettres:
            cible = dfa.transitions.get((e, c))
            if cible is not None:
                mini.transitions[(groupe[e], c)] = groupe[cible]
    return mini