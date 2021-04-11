import random
import hashlib, binascii, os

def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

# ouvre aleatoire.txt en mode lecture
# change le contenu pour que ca devient une liste
with open('c:/Users/vinla/Larevel/MySQL/titres.txt', 'r') as titres:
    listeTitre = titres.read().splitlines()

# ouvre auteurs.txt en mode lecture
# change le contenu pour que ca devient une liste
with open('c:/Users/vinla/Larevel/MySQL/auteurs.txt', 'r') as auteurs:
    listeAuteur = auteurs.read().splitlines()

# ouvre usernames.txt en mode lecture
# change le contenu pour que ca devient une liste
with open("c:/Users/vinla/Larevel/MySQL/usernames.txt", 'r') as usernames:
    listeUsername = usernames.read().splitlines()

# ouvre passwordsBase.txt en mode lecture
# change le contenu pour que ca devient une liste
with open("c:/Users/vinla/Larevel/MySQL/passwordsBase.txt", 'r') as passwordsBase:
    listePasswordBase = passwordsBase.read().splitlines()

# ouvre passwordsBase.txt en mode ecriture
# hash chaque password de listePasswordBase
# ecris le resultat dans passwordsHashed.txt
with open("c:/Users/vinla/Larevel/MySQL/passwordsHashed.txt", 'w') as passwordsHashed:
    for i in range(0, 100):
        hashed = hash_password(listePasswordBase[i])+"\n"
        passwordsHashed.write(hashed)

# ouvre passwordsHashed.txt en mode lecture
# change le contenu pour que ca devient une liste
with open("c:/Users/vinla/Larevel/MySQL/passwordsHashed.txt",'r') as passwordsHashed:
    listePasswordHashed = passwordsHashed.read().splitlines()

# ouvre nom_clients.txt en mode lecture
# change le contenu pour que ca devient une liste
with open("c:/Users/vinla/Larevel/MySQL/nom_clients.txt",'r') as nom_clients:
    listeNomClient = nom_clients.read().splitlines()

# ouvre courriels.txt en mode lecture
# change le contenu pour que ca devient une liste
with open("c:/Users/vinla/Larevel/MySQL/courriels.txt",'r') as courriels:
    listeCourriel = courriels.read().splitlines()

# ouvre couvertures.txt en mode lecture
# change le contenu pour que ca devient une liste
with open("c:/Users/vinla/Larevel/MySQL/couvertures.txt",'r') as couvertures:
    listeCouvertures = couvertures.read().splitlines()

genre = ['Roman', 'Polar', 'Theatre', 'Poesie', 'Science-fiction']
annee = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
typeCouverture = ['souple', 'rigide']
bid = [1, 2, 3, 4, 5]
quantite = [1, 2, 3]
prix = [9.99, 14.99, 19.99, 24.99, 29.99]


# ouvre catalogue.txt qui se trouve dans le meme dossier que ce .py,  ou le créer si ce fichier n'existe pas
# en mode ecriture
with open('c:/Users/vinla/Larevel/MySQL/catalogue.txt', 'w') as catalogue:
    for i in range(1, 101):
        ligne = ("(" + str(i) + ", " + '''"''' + listeTitre[i-1] + '''"''' + ", " + '''"''' + 
        listeAuteur[i-1] + '''"''' + ", " + '''"''' + random.choice(genre) + '''"''' + ", " + 
        random.choice(annee) + ", " + '''"''' + listeCouvertures[i-1] + '''"''' + ")\n")
        catalogue.write(ligne)

# ouvre inventaire.txt qui se trouve dans le meme dossier que ce .py,  ou le créer si ce fichier n'existe pas
# en mode ecriture
with open('c:/Users/vinla/Larevel/MySQL/inventaire.txt', 'w') as inventaire:
    for i in range(1, 101):
        ligne = ("(" + str(i) + ", " + str(random.choice(bid)) + ", " + str(random.choice(quantite)) + 
        ", " + '''"''' + random.choice(typeCouverture) + '''"''' + ", " + 
        str(random.choice(prix)) + ")\n")
        inventaire.write(ligne)

# ouvre clients.txt qui se trouve dans le meme dossier que ce .py,  ou le créer si ce fichier n'existe pas
# en mode ecriture
with open('c:/Users/vinla/Larevel/MySQL/clients.txt', 'w') as clients:
    for i in range(1, 101):
        ligne = ("(" + '''"''' + listeUsername[i-1] + '''"''' + ", " + '''"''' + listePasswordHashed[i-1] + 
        '''"''' + ", " + '''"''' + listeNomClient[i-1] + '''"''' + ", " + '''"''' + 
        listeCourriel[i-1] + '''"''' + ")\n")
        clients.write(ligne)