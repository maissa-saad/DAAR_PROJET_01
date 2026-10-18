# Projet 1 – Automates : clone de egrep avec support partiel des ERE

**Collaboratrices :** Ndeye Awa Dieme, Maïssa Saad
**Enseignant :** BM Bui-Xuan
**UE :** DAAR – Sorbonne Université, 2026-2027

Ce programme cherche un motif (une expression régulière) dans un fichier texte
et affiche toutes les lignes qui le contiennent, comme la commande `egrep`.

## Expressions régulières acceptées

| Élément | Exemple | Sens |
|---|---|---|
| lettre | `a` | le caractère lui-même (tout caractère qui n'est pas un opérateur) |
| point | `a.c` | n'importe quel caractère |
| concaténation | `abc` | a puis b puis c |
| alternative | `chat\|chien` | l'un ou l'autre |
| étoile | `ab*` | zéro, une ou plusieurs fois |
| plus | `ab+` | une ou plusieurs fois |
| parenthèses | `(ab)*` | groupement |

## Prérequis

- Python 3.8 ou plus récent
- `make`
- Pour les tests et les benchmarks seulement : `pytest` et `matplotlib`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest matplotlib
```

## Compilation

```bash
make
```

Cette commande crée l'exécutable `myegrep` à la racine du projet.

## Utilisation

```bash
./myegrep "<regex>" <fichier>
```

Mettez toujours la regex entre guillemets, sinon le terminal interprète
lui-même les caractères `*`, `|`, `(` et `)`.

**Exemples :**

```bash
./myegrep "Sargon" tests/data/petit.txt          # mot simple : recherche avec KMP
./myegrep "S(a|g|r)+on" tests/data/56667-0.txt   # regex : recherche avec l'automate
./myegrep "(K|k)ing" tests/data/petit.txt
```

**Codes de retour (identiques à egrep) :**

| Code | Signification |
|---|---|
| 0 | au moins une ligne trouvée |
| 1 | aucune ligne trouvée |
| 2 | erreur : regex mal formée, regex vide ou fichier introuvable |

## Tests

**1. Télécharger le livre de test** (projet Gutenberg) :

```bash
tests/download.sh
```

**2. Lancer tous les tests :**

```bash
make test
```

Cette commande lance :
- les tests unitaires de chaque étape (parseur, NFA, DFA, minimisation, KMP) ;
- le test de conformité, qui compare la sortie et le code de retour de
  `myegrep` avec ceux de `grep -E` sur 11 motifs et 2 fichiers.

**3. Comparer à la main avec egrep :**

```bash
./myegrep "S(a|g|r)+on" tests/data/56667-0.txt > mon_resultat.txt
grep -E   "S(a|g|r)+on" tests/data/56667-0.txt > vrai_resultat.txt
diff mon_resultat.txt vrai_resultat.txt && echo "IDENTIQUE"
```

## Benchmarks

```bash
PYTHONPATH=. python3 bench/benchmark.py
```

Les graphiques sont enregistrés dans `bench/results/` :
- `1_methodes.png` : automate, KMP et egrep sur le motif `Sargon` ;
- `2_taille.png` : temps selon la taille du fichier ;
- `3_regex.png` : temps de l'automate selon la forme de la regex.

## Organisation du code

```
src/
├── parser.py     regex -> arbre syntaxique (descente récursive)
├── nfa.py        arbre -> automate non déterministe (Thompson)
├── dfa.py        NFA -> automate déterministe (sous-ensembles)
├── minimize.py   minimisation de l'automate (Moore)
├── matcher.py    recherche du motif dans une ligne
├── kmp.py        recherche d'un mot simple (Knuth-Morris-Pratt)
└── myegrep.py    point d'entrée : choix de la méthode et lecture du fichier
tests/            tests unitaires, test de conformité, fichiers de test
bench/            benchmarks et graphiques
rapport/          rapport du projet
```

## Nettoyage

```bash
make clean
```
