from src.parser import parse
from src.nfa import arbre_vers_nfa, accepte
from src.dfa import construire_dfa, accepte_dfa


def test_a_etoile_deux_etats():
    dfa = construire_dfa(arbre_vers_nfa(parse("a*")))
    assert dfa.nb_etats == 2          # D0 et D1, comme a la main
    assert len(dfa.finaux) == 2


def test_dfa_meme_reponse_que_nfa():
    regex_a_tester = ["a", "abc", "a|bc", "a*", "(ab)*", "a.c", "S(a|g|r)+on"]
    mots = ["", "a", "b", "ab", "abc", "bc", "aaa", "abab", "a9c", "azc",
            "Sargon", "Saon", "Son", "sargon"]
    for regex in regex_a_tester:
        nfa = arbre_vers_nfa(parse(regex))
        dfa = construire_dfa(nfa)
        for mot in mots:
            assert accepte_dfa(dfa, mot) == accepte(nfa, mot), regex + " / " + mot