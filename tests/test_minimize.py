from src.parser import parse
from src.nfa import arbre_vers_nfa
from src.dfa import construire_dfa, accepte_dfa
from src.minimize import minimiser


def dfa_de(regex):
    return construire_dfa(arbre_vers_nfa(parse(regex)))


def test_exemple_ab_cb():
    dfa = dfa_de("ab|cb")
    assert dfa.nb_etats == 5
    assert minimiser(dfa).nb_etats == 3     # comme a la main


def test_a_ou_b():
    assert minimiser(dfa_de("a|b")).nb_etats == 2


def test_minimal_meme_reponse():
    regex_a_tester = ["a", "abc", "a|bc", "a*", "(ab)*", "a.c", "ab|cb", "S(a|g|r)+on"]
    mots = ["", "a", "b", "ab", "cb", "abc", "bc", "aaa", "abab", "a9c",
            "Sargon", "Saon", "Son"]
    for regex in regex_a_tester:
        dfa = dfa_de(regex)
        mini = minimiser(dfa)
        assert mini.nb_etats <= dfa.nb_etats
        for mot in mots:
            assert accepte_dfa(mini, mot) == accepte_dfa(dfa, mot), regex + " / " + mot