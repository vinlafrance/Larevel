from flask import Flask, render_template, request
import pymysql, pymysql.cursors
import hashlib, binascii, os

def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    #Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

app = Flask(__name__)
ProfilUtilisateur = {"username" : "", "nom" : "", "courriel" : ""}
Gerant = {"nom" : ""}

@app.route("/")
def main():
    return render_template("Accueil_non_connecte.html")

@app.route("/Accueil")
def Accueil():
    if ProfilUtilisateur["username"] != "":
        return render_template("Accueil_connecte.html")
    return render_template("Accueil_non_connecte.html")

@app.route("/ConnexionTest", methods=['POST'])
def ConnexionTest():
    username = '"' + request.form.get('username') + '"'
    password = request.form.get('password')
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='SELECT password FROM Clients WHERE username='+username+';'
    cur=conn.cursor()
    cur.execute(cmd)
    passeVrai = cur.fetchone()
    if (passeVrai!=None) and (verify_password(passeVrai[0], password)):
        cmd='SELECT * FROM Clients WHERE username='+username+';'
        cur=conn.cursor()
        cur.execute(cmd)
        info = cur.fetchone()
        global ProfilUtilisateur
        ProfilUtilisateur["username"]=username
        ProfilUtilisateur["nom"]=info[2]
        ProfilUtilisateur["courriel"]=info[3]
        return render_template('Connexion_succes.html', profil=ProfilUtilisateur) 
    return render_template("Connexion.html", message="Informations invalides!")

@app.route("/Catalogue")
def Catalogue():
    catalogue = []
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='SELECT * FROM Catalogue;'
    cur=conn.cursor()
    cur.execute(cmd)
    for i in range(cur.rowcount):
        item = cur.fetchone()
        catalogue.append({"titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4]})
    return render_template("Catalogue.html", catalogue=catalogue)

@app.route("/PourRecherche", methods=['POST'])
def PourRecherche():
    titreRecherche = request.form.get('titreRecherche')
    conn = pymysql.connect(host='localhost', user='root', password='', db='larevel', charset='utf8mb4',
                           autocommit=True)
    cmd = """SELECT titre FROM Catalogue WHERE titre LIKE '%{}%'""".format(titreRecherche)
    cmd += ";"
    cur = conn.cursor()
    cur.execute(cmd)
    titrelivre = cur.fetchone()
    catalogueRecherche = []
    if (titrelivre!=None):
        conn = pymysql.connect(host='localhost', user='root', password='', db='larevel', charset='utf8mb4',
                               autocommit=True)
        cmd = """SELECT * FROM Catalogue WHERE titre LIKE '%{}%'""".format(titreRecherche)
        cmd += ";"
        cur = conn.cursor()
        cur.execute(cmd)
        for i in range(cur.rowcount):
            item = cur.fetchone()
            catalogueRecherche.append({"titre": item[1], "auteur": item[2], "genre": item[3], "annee": item[4]})
        return render_template('catalogueRecherche.html', catalogueRecherche=catalogueRecherche)
    return render_template("Catalogue.html") # message="Nous n'avons pas ce livre malheureusement"

@app.route("/Connexion")
def Connection():
    return render_template("Connexion.html")

@app.route("/Description")
def Description():
    return render_template("Description.html")

@app.route("/Gerants")
def ConnexionGerants():
    return render_template("ConnexionGerants.html")

@app.route("/GerantsTest", methods=['POST'])
def GerantsTest():
    nom_gerant = '"' + request.form.get('nom_gerant') + '"'
    gid = request.form.get('gid')
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='SELECT gid FROM Gerants WHERE nom='+nom_gerant+';'
    cur=conn.cursor()
    cur.execute(cmd)
    gidVrai = cur.fetchone()
    if (gidVrai!=None) and (int(gidVrai[0]) == int(gid)):
        cmd='SELECT * FROM Gerants WHERE nom='+nom_gerant+';'
        cur=conn.cursor()
        cur.execute(cmd)
        info = cur.fetchone()
        global Gerant
        Gerant["nom"]=info[1]
        return render_template('ConnexionGerants_succes.html', gerant=Gerant) 
    return render_template("ConnexionGerants.html", message="Informations invalides!")

@app.route("/Inscription")
def Inscription():
    return render_template("Inscription.html")

@app.route("/Panier")
def Panier():
    return render_template("Panier.html")

@app.route("/Profil")
def Profil():
    return render_template("Profil.html", profil=ProfilUtilisateur)

@app.route("/ProfilGerant")
def ProfilGerant():
    return render_template("ProfilGerant.html", gerant=Gerant)

@app.route("/Deconnexion")
def Deconnexion():
    global ProfilUtilisateur
    ProfilUtilisateur = {"username" : "", "nom" : "", "courriel" : ""}
    global Gerant
    Gerant = {"nom" : ""}
    return render_template("Deconnexion.html")

@app.route("/InscriptionTest", methods=['POST'])
def InscriptionTest():
    username = '"' + request.form.get("username") + '"'
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='SELECT * FROM Clients WHERE username='+username+';'
    cur=conn.cursor()
    cur.execute(cmd)
    info = cur.fetchone()
    if info != None:
        return render_template("Inscription.html", message="Ce username existe déjà!")
    password = '"' + hash_password(request.form.get("password")) + '"'
    nom = '"' + request.form.get("nom") + '"'
    courriel = '"' + request.form.get("courriel") + '"'
    cmd='INSERT INTO Clients VALUE ('+username+', '+password+', '+nom+', '+courriel+');'
    cur=conn.cursor()
    cur.execute(cmd)
    return render_template("Inscription.html", message="Félicitation, vous êtes maintenant inscrit!")

@app.route("/Inventaire")
def Inventaire():
    inventaire = []
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='select titre, auteur, genre, annee, ville, type, quantite, prix from Inventaire I, Catalogue C, Boutiques B WHERE I.lid = C.lid and B.bid = I.bid;'
    cur=conn.cursor()
    cur.execute(cmd)
    for i in range(100):
        item = cur.fetchone()
        inventaire.append({"titre" : item[0], "auteur" : item[1], "genre" : item[2], "annee" : item[3], "ville" : item[4], "type" : item[5], "quantite" : item[6], "prix" : item[7]})
    return render_template("Inventaire.html", inventaire=inventaire)

if __name__ == "__main__":
    app.run()

