import random

# ouvre aleatoire.txt en mode lecture
# change le contenu pour que ca devient une liste
with open('aleatoire.txt', 'r') as aleatoire:
    listetitre = aleatoire.read().splitlines()

with open('auteurs.txt', 'r') as auteurs:
    listeauteur = auteurs.read().splitlines()

genre = ['Roman', 'Polar', 'Theatre', 'Poesie', 'Science-fiction']
annee = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

# ouvre fichier.txt qui se trouve dans le meme dossier que ce .py,  ou le créer si ce fichier n'existe pas
# en mode ecriture
# OU f = open('fichier.txt', 'w')
#    f.close()  a la fin
with open('fichier.txt', 'w') as f:
    for i in range(1, 101):
        ligne = "(" + str(i) + ", " + '''"''' + random.choice(listetitre) + '''"''' + ", " + '''"''' + random.choice(
            listeauteur) + '''"''' + ", " + '''"''' + random.choice(genre) + '''"''' + ", " + random.choice(
            annee) + "),\n"
        f.write(ligne)