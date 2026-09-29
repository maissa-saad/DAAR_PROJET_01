class Parser:

    def __init__(self, regex):
        self.regex = regex
        self.pos = 0
        
    def courant(self):
        if self.pos < len(self.regex):
            return self.regex[self.pos]
        return None
    
    def avancer(self):
        self.pos += 1
        
    def parse_atome(self):

        caractere = self.courant()

        # cas d'une lettre ASCII
        if caractere is not None and (('a' <= caractere <= 'z') or ('A' <= caractere <= 'Z')):
            self.avancer()
            return caractere

        # cas du point
        if caractere == '.':
            self.avancer()
            return caractere

        # cas de la parenthese ouverte
        if caractere == '(':
            self.avancer()

            expression = self.parse_alternative()

            if self.courant() != ')':
                raise ValueError("Parenthese fermante manquante")

            self.avancer()

            return expression

        # sinon erreur
        raise ValueError("Atome invalide")
    
    def parse_repetition(self):

        # on commence par lire un atome
        atome = self.parse_atome()

        # on regarde si l'atome est suivi de *
        


def parser(regex):

    # cette fonction va prendre en entrée une chaine de caractères
    # et analyser si elle correspond à la grammaire des regex autorisées
    #
    # exemple de INPUT : (a|b)*
    #
    # si la regex est valide, la fonction construit une structure
    # qui représente la regex
    #
    # si la regex n'est pas valide, la fonction renvoie une erreur
    #
    # le programme doit refuser certaines formes, par exemple :
    # a| , * , *a , |a , () , a** , (a
    #
    # cette fonction doit aussi respecter l'ordre de priorité défini :
    # 1. etoile
    # 2. concatenation
    # 3. alternative

    return 1


"""
Les caractères autorisés :

    lettre_ascii
    parenthese_ouverte
    parenthese_fermee
    alternative
    operation_etoile
    point

Les opérations :

    concatenation


La grammaire :

    expression : alternative

    alternative : concatenation
                | concatenation alternative

    concatenation : repetition
                  | repetition concatenation

    repetition : atome
               | atome etoile

    atome : lettre_ascii
          | point
          | parenthese_ouverte expression parenthese_fermee
          
Pour la précision : Dans notre projet, un atome est une regex qui représente une seule unité de base
"""