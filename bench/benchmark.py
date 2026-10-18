# ============================================================
# Benchmarks : automate vs KMP vs egrep
# Prerequis : tests/download.sh (livre) et matplotlib
# Lancer depuis la racine du projet :
#     PYTHONPATH=. python3 bench/benchmark.py
# Les graphiques sont enregistres dans bench/results/
# ============================================================

import os
import time
import statistics
import subprocess
import matplotlib
matplotlib.use("Agg")                 # pas de fenetre : on enregistre en .png
import matplotlib.pyplot as plt

from src.parser import parse
from src.nfa import arbre_vers_nfa
from src.dfa import construire_dfa
from src.minimize import minimiser
from src.matcher import ligne_correspond
from src.kmp import kmp

LIVRE = "tests/data/56667-0.txt"
REPETITIONS = 10
LEGENDE = ("Moyenne sur " + str(REPETITIONS)
           + " executions - traits noirs : ecart-type")
os.makedirs("bench/results", exist_ok=True)
os.makedirs("bench/data", exist_ok=True)


def lire_lignes(chemin):
    """Lit le fichier et renvoie la liste de ses lignes (sans le \\n)."""
    with open(chemin, encoding="utf-8", errors="replace", newline="") as f:
        lignes = []
        for ligne in f:
            lignes.append(ligne.rstrip("\n"))
        return lignes


# ---------- Une mesure pour chaque methode ----------

def temps_automate(regex, lignes):
    """Temps pour construire l'automate puis tester toutes les lignes."""
    debut = time.perf_counter()
    dfa = minimiser(construire_dfa(arbre_vers_nfa(parse(regex))))
    for ligne in lignes:
        ligne_correspond(dfa, ligne)
    return time.perf_counter() - debut


def temps_kmp(motif, lignes):
    """Temps pour tester toutes les lignes avec KMP."""
    debut = time.perf_counter()
    for ligne in lignes:
        kmp(motif, ligne)
    return time.perf_counter() - debut


def temps_egrep(regex, chemin):
    """Temps d'execution du vrai egrep.
    capture_output=True : on recupere la sortie, ce qui oblige grep a lire
    tout le fichier (avec /dev/null, grep s'arrete a la premiere ligne trouvee)."""
    debut = time.perf_counter()
    subprocess.run(["grep", "-E", regex, chemin], capture_output=True)
    return time.perf_counter() - debut


def moyenne_ecart(temps):
    """Renvoie (moyenne, ecart-type) d'une liste de temps."""
    return statistics.mean(temps), statistics.stdev(temps)


def ecrire_valeurs(batons, moyennes):
    """Ecrit la valeur au-dessus de chaque baton (ex : 153.5 ms)."""
    etiquettes = []
    for m in moyennes:
        etiquettes.append(str(round(m, 1)) + " ms")
    plt.bar_label(batons, labels=etiquettes, padding=4)


# ---------- Experience 1 : motif litteral, 3 methodes ----------

def experience_1():
    motif = "Sargon"
    lignes = lire_lignes(LIVRE)

    # on repete chaque methode REPETITIONS fois
    t_auto, t_kmp, t_egrep = [], [], []
    for i in range(REPETITIONS):
        t_auto.append(temps_automate(motif, lignes))
        t_kmp.append(temps_kmp(motif, lignes))
        t_egrep.append(temps_egrep(motif, LIVRE))

    # moyenne et ecart-type de chaque methode, en millisecondes
    noms = ["Automate", "KMP", "egrep"]
    moyennes, ecarts = [], []
    for t in [t_auto, t_kmp, t_egrep]:
        m, e = moyenne_ecart(t)
        moyennes.append(m * 1000)
        ecarts.append(e * 1000)

    print("Experience 1 (ms) :", dict(zip(noms, moyennes)))

    # graphique en batons
    plt.figure()
    batons = plt.bar(noms, moyennes, yerr=ecarts, capsize=5)
    ecrire_valeurs(batons, moyennes)
    plt.ylim(0, max(moyennes) * 1.2)          # place pour les valeurs en haut
    plt.ylabel("Temps (ms)")
    plt.title("Motif 'Sargon' sur le livre 56667")
    plt.figtext(0.5, 0.01, LEGENDE, ha="center", fontsize=8)
    plt.tight_layout(rect=[0, 0.04, 1, 1])    # laisse de la place pour la legende
    plt.savefig("bench/results/1_methodes.png")
    plt.close()


# ---------- Experience 2 : taille du fichier ----------

def experience_2():
    motif = "Sargon"
    with open(LIVRE, encoding="utf-8", newline="") as f:
        texte = f.read()

    facteurs = [1, 2, 4, 8]
    courbes = {"Automate": [], "KMP": [], "egrep": []}

    for k in facteurs:
        # on cree un fichier qui contient le livre recopie k fois
        chemin = "bench/data/livre_x" + str(k) + ".txt"
        with open(chemin, "w", encoding="utf-8", newline="") as f:
            f.write(texte * k)
        lignes = lire_lignes(chemin)

        t_auto, t_kmp, t_egrep = [], [], []
        for i in range(REPETITIONS):
            t_auto.append(temps_automate(motif, lignes))
            t_kmp.append(temps_kmp(motif, lignes))
            t_egrep.append(temps_egrep(motif, chemin))
        courbes["Automate"].append(statistics.mean(t_auto) * 1000)
        courbes["KMP"].append(statistics.mean(t_kmp) * 1000)
        courbes["egrep"].append(statistics.mean(t_egrep) * 1000)

    print("Experience 2 (ms) :", courbes)

    # graphique en courbes
    plt.figure()
    for nom in courbes:
        plt.plot(facteurs, courbes[nom], marker="o", label=nom)
        # ecrire la valeur a cote de chaque point
        for i in range(len(facteurs)):
            plt.annotate(str(round(courbes[nom][i])) + " ms",
                         (facteurs[i], courbes[nom][i]),
                         textcoords="offset points", xytext=(5, 5), fontsize=8)
    plt.xticks(facteurs)
    plt.xlabel("Taille du fichier (x fois le livre)")
    plt.ylabel("Temps (ms)")
    plt.title("Temps de recherche selon la taille du fichier")
    plt.legend()
    plt.figtext(0.5, 0.01, "Moyenne sur " + str(REPETITIONS) + " executions",
                ha="center", fontsize=8)
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig("bench/results/2_taille.png")
    plt.close()


# ---------- Experience 3 : forme de la regex (automate) ----------

def experience_3():
    regex_a_tester = ["Sargon", "S(a|g|r)+on", "Babylon|Assyria",
                      "(K|k)ing", "Eu.hrates", "a*"]
    lignes = lire_lignes(LIVRE)

    moyennes, ecarts = [], []
    for regex in regex_a_tester:
        t = []
        for i in range(REPETITIONS):
            t.append(temps_automate(regex, lignes))
        m, e = moyenne_ecart(t)
        moyennes.append(m * 1000)
        ecarts.append(e * 1000)

    print("Experience 3 (ms) :", dict(zip(regex_a_tester, moyennes)))

    # graphique en batons
    plt.figure(figsize=(8, 4))
    batons = plt.bar(regex_a_tester, moyennes, yerr=ecarts, capsize=5)
    ecrire_valeurs(batons, moyennes)
    plt.ylim(0, max(moyennes) * 1.2)
    plt.ylabel("Temps (ms)")
    plt.title("Automate : temps selon la regex")
    plt.xticks(rotation=20)
    plt.figtext(0.5, 0.01, LEGENDE, ha="center", fontsize=8)
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig("bench/results/3_regex.png")
    plt.close()


if __name__ == "__main__":
    if not os.path.exists(LIVRE):
        raise SystemExit("Livre absent : lancer d'abord tests/download.sh")
    experience_1()
    experience_2()
    experience_3()
    print("Graphiques enregistres dans bench/results/")