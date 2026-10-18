import random
from src.kmp import kmp, construire_lps

def test_lps_abab():
    assert construire_lps("abab") == [0, 0, 1, 2]

def test_kmp_aleatoire():
    random.seed(0)
    for _ in range(2000):
        motif = "".join(random.choice("ab") for _ in range(random.randint(1, 4)))
        texte = "".join(random.choice("ab") for _ in range(random.randint(0, 15)))
        assert kmp(motif, texte) == (motif in texte), (motif, texte)