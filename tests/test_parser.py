from src.parser import parse, afficher


def test_lettre():
    assert afficher(parse("a")) == "a"

def test_concatenation():
    assert afficher(parse("abc")) == "·(·(a,b),c)"

def test_etoile():
    assert afficher(parse("ab*")) == "·(a,*(b))"

def test_alternative():
    assert afficher(parse("a|b|c")) == "|(|(a,b),c)"

def test_parentheses():
    assert afficher(parse("(ab)*")) == "*(·(a,b))"

def test_point():
    assert afficher(parse("a.c")) == "·(·(a,.),c)"

def test_plus():
    assert afficher(parse("a+")) == "·(a,*(a))"

def test_erreurs():
    mauvaises = ["", "a|", "(ab", "ab)", "*a", "()"]
    for regex in mauvaises:
        try:
            parse(regex)
            assert False, regex + " aurait du donner une erreur"
        except ValueError:
            pass   # c'est le comportement attendu