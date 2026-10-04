from src.parser import parse
from src.nfa import arbre_vers_nfa, accepte


def test_lettre():
    nfa = arbre_vers_nfa(parse("a"))
    assert nfa.nb_etats == 2
    assert nfa.transitions == [(0, "a", 1)]
    assert nfa.debut == 0 and nfa.fin == 1

def test_concat():
    nfa = arbre_vers_nfa(parse("ab"))
    assert nfa.nb_etats == 4               # 2 lettres x 2 etats, 0 pour la concat
    assert (1, "EPS", 2) in nfa.transitions
    assert nfa.debut == 0 and nfa.fin == 3

def test_alt():
    nfa = arbre_vers_nfa(parse("a|b"))
    assert nfa.nb_etats == 6               # 2 + 2 + 2
    assert nfa.debut == 4 and nfa.fin == 5
    assert (4, "EPS", 0) in nfa.transitions
    assert (4, "EPS", 2) in nfa.transitions

def test_etoile():
    nfa = arbre_vers_nfa(parse("a*"))
    assert nfa.nb_etats == 4
    assert (1, "EPS", 0) in nfa.transitions   # recommencer
    assert (2, "EPS", 3) in nfa.transitions   # sauter

def test_point():
    nfa = arbre_vers_nfa(parse("."))
    assert nfa.transitions == [(0, "DOT", 1)]

def test_exemple_enonce():
    nfa = arbre_vers_nfa(parse("S(a|g|r)+on"))
    assert nfa.nb_etats > 0


def verifie(regex, acceptes, refuses):
    nfa = arbre_vers_nfa(parse(regex))
    for mot in acceptes:
        assert accepte(nfa, mot), regex + " devrait accepter " + mot
    for mot in refuses:
        assert not accepte(nfa, mot), regex + " devrait refuser " + mot

def test_accepte_lettre():
    verifie("a", ["a"], ["", "b", "aa"])

def test_accepte_concat():
    verifie("abc", ["abc"], ["ab", "abcd", "acb"])

def test_accepte_alt():
    verifie("a|bc", ["a", "bc"], ["b", "abc", ""])

def test_accepte_etoile():
    verifie("a*", ["", "a", "aaaa"], ["b", "ab"])

def test_accepte_parentheses():
    verifie("(ab)*", ["", "ab", "abab"], ["a", "aba", "ba"])

def test_accepte_point():
    verifie("a.c", ["abc", "a9c", "a c"], ["ac", "abbc"])

def test_accepte_exemple_enonce():
    verifie("S(a|g|r)+on", ["Sargon", "Saon", "Sgrraon"], ["Son", "sargon", "Sargo"])