# pylint: disable=unused-variable
# pylint: enable=too-many-lines

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
GerantActif = {"username" : "", "nom" : "", "courriel" : "", "bid" : ""}

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
    cmd = "SELECT COUNT(lid) FROM Catalogue;"
    count = conn.cursor()
    count.execute(cmd)
    nb = count.fetchone()
    for i in range(nb[0]):
        item = cur.fetchone()
        catalogue.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "couverture" : item[5]})
    return render_template("Catalogue.html", catalogue=catalogue)

@app.route("/CatalogueRecherche", methods=['POST'])
def PourRecherche():
    catalogue = []
    titreRecherche = request.form.get('titreRecherche')
    conn = pymysql.connect(host='localhost', user='root', password='', db='larevel', charset='utf8mb4', autocommit=True)
    cmd = "SELECT * FROM Catalogue WHERE titre LIKE '%"+titreRecherche+"%';"
    cur = conn.cursor()
    cur.execute(cmd)
    infos = cur
    cmd = "SELECT COUNT(titre) FROM Catalogue WHERE titre LIKE '%"+titreRecherche+"%';"
    cur = conn.cursor()
    cur.execute(cmd)
    nbTitres = cur.fetchone()
    if nbTitres[0] == 0:
        return render_template("Catalogue.html", catalogue=catalogue, message="Aucun résultat ne correspond à la recherche.")
    for i in range(nbTitres[0]):
        item = infos.fetchone()
        catalogue.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "couverture" : item[5]})
    return render_template("Catalogue.html", catalogue=catalogue, nbTitres=nbTitres[0])

@app.route("/Connexion")
def Connection():
    return render_template("Connexion.html")

@app.route('/Description<int:item_id>')
def Description(item_id):
    inventaire = []
    conn = pymysql.connect(host='localhost', user='root', password='', db='larevel', charset='utf8mb4', autocommit=True)
    cmd = 'SELECT * FROM Catalogue WHERE lid='+str(item_id)+';'
    cur = conn.cursor()
    cur.execute(cmd)
    item = cur.fetchone()
    catalogue = {"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "couverture" : item[5]}
    cmd = 'select I.lid, titre, auteur, genre, annee, ville, type, quantite, prix, B.bid from Inventaire I, Catalogue C, Boutiques B WHERE I.lid = '+str(item_id)+' and I.lid = C.lid and B.bid = I.bid;'
    inv = conn.cursor()
    inv.execute(cmd)
    cmd = 'SELECT COUNT(lid) FROM Inventaire WHERE lid='+str(item_id)+';'
    cur = conn.cursor()
    cur.execute(cmd)
    nb = cur.fetchone()
    if nb[0] == 0:
        return render_template("Description.html", catalogue=catalogue, message="Cet article n'est plus en stock.")
    for i in range(nb[0]):
        item = inv.fetchone()
        inventaire.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "ville" : item[5], "type" : item[6], "quantite" : item[7], "prix" : item[8], "bid" : item[9]})
    return render_template("Description.html", catalogue=catalogue, inventaire=inventaire)

@app.route("/Gerants")
def ConnexionGerants():
    return render_template("ConnexionGerants.html")

@app.route("/GerantsTest", methods=['POST'])
def GerantsTest():
    username = '"' + request.form.get('username') + '"'
    password = request.form.get('password')
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='SELECT password FROM Clients WHERE username='+username+';'
    cur=conn.cursor()
    cur.execute(cmd)
    passeVrai = cur.fetchone()
    if (passeVrai!=None) and (verify_password(passeVrai[0], password)):
        cmd='SELECT G.nom FROM Gerants G, Clients C WHERE C.username='+username+' and C.nom = G.nom;'
        cur=conn.cursor()
        cur.execute(cmd)
        nomVrai = cur.fetchone()
        if (nomVrai!=None) :
            cmd='SELECT C.nom, C.courriel, B.bid FROM Clients C, Boutiques B, Gerants G WHERE C.username='+username+' and C.nom = G.nom and G.gid = B.gid;'
            cur=conn.cursor()
            cur.execute(cmd)
            info = cur.fetchone()
            global GerantActif
            GerantActif["username"]=username
            GerantActif["nom"]=info[0]
            GerantActif["courriel"]=info[1]
            GerantActif["bid"]=info[2]
            return render_template('ConnexionGerants_succes.html', profil=GerantActif) 
    return render_template("ConnexionGerants.html", message="Informations invalides!")

@app.route("/Inscription")
def Inscription():
    return render_template("Inscription.html")

@app.route("/Panier")
def Panier():
    PanierUtilisateur = []
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='select P.lid, titre, auteur, genre, annee, ville, P.type, P.quantite, P.prix, P.bid, couverture from Catalogue C, Boutiques B, Panier P WHERE P.username='+ProfilUtilisateur["username"]+' and P.lid = C.lid and B.bid = P.bid;'
    cur=conn.cursor()
    cur.execute(cmd)
    cmd='select count(lid) from Panier where username='+ProfilUtilisateur["username"]+';'
    count = conn.cursor()
    count.execute(cmd)
    nb = count.fetchone()
    if nb[0] != 0 :
        for i in range(nb[0]):
            item = cur.fetchone()
            PanierUtilisateur.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "ville" : item[5], "type" : item[6], "quantite" : item[7], "prix" : item[8], "bid" : item[9], "couverture" : item[10]})
        return render_template("Panier.html", panier=PanierUtilisateur)
    return render_template("Panier.html", message="Aucun item dans le panier.")

@app.route("/PanierAjout<int:item_id>_<int:boutique_id>_<string:item_type>_<float:item_prix>")
def PanierAjout(item_id, boutique_id, item_type, item_prix):
    PanierUtilisateur = []
    global ProfilUtilisateur
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd="select * from panier where username="+ProfilUtilisateur["username"]+" and lid="+str(item_id)+" and bid="+str(boutique_id)+" and type='"+item_type+"';"
    cur = conn.cursor()
    cur.execute(cmd)
    infos = cur.fetchone()
    if infos!=None:
        cmd="select quantite from inventaire where lid="+str(item_id)+" and bid="+str(boutique_id)+" and type='"+item_type+"';"
        qty = conn.cursor()
        qty.execute(cmd)
        quantite = qty.fetchone()
        if infos[3] == quantite[0]:
            inventaire = []
            cmd = 'SELECT * FROM Catalogue WHERE lid='+str(item_id)+';'
            cur = conn.cursor()
            cur.execute(cmd)
            item = cur.fetchone()
            catalogue = {"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "couverture" : item[5]}
            cmd = 'select I.lid, titre, auteur, genre, annee, ville, type, quantite, prix, B.bid from Inventaire I, Catalogue C, Boutiques B WHERE I.lid = '+str(item_id)+' and I.lid = C.lid and B.bid = I.bid;'
            inv = conn.cursor()
            inv.execute(cmd)
            cmd = 'SELECT COUNT(lid) FROM Inventaire WHERE lid='+str(item_id)+';'
            cur = conn.cursor()
            cur.execute(cmd)
            nb = cur.fetchone()
            for i in range(nb[0]):
                item = inv.fetchone()
                inventaire.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "ville" : item[5], "type" : item[6], "quantite" : item[7], "prix" : item[8], "bid" : item[9]})
            return render_template("Description.html", catalogue=catalogue, inventaire = inventaire, insuffisant="Nombre d'exemplaires insuffisant en stock.")
        cmd="update panier set quantite="+str(infos[3]+1)+" where username="+ProfilUtilisateur["username"]+" and lid="+str(item_id)+" and bid="+str(boutique_id)+" and type='"+item_type+"';"
        cur = conn.cursor()
        cur.execute(cmd)
    else:
        cmd="insert into panier value ("+ProfilUtilisateur["username"]+", "+str(item_id)+", "+str(boutique_id)+", 1, '"+item_type+"', "+str(item_prix)+");"
        cur = conn.cursor()
        cur.execute(cmd)
    cmd='select P.lid, titre, auteur, genre, annee, ville, P.type, P.quantite, P.prix, P.bid, couverture from Catalogue C, Boutiques B, Panier P WHERE P.username='+ProfilUtilisateur["username"]+' and P.lid = C.lid and B.bid = P.bid;'
    cur=conn.cursor()
    cur.execute(cmd)
    cmd='select count(lid) from Panier where username='+ProfilUtilisateur["username"]+';'
    count = conn.cursor()
    count.execute(cmd)
    nb = count.fetchone()
    for i in range(nb[0]):
        item = cur.fetchone()
        PanierUtilisateur.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "ville" : item[5], "type" : item[6], "quantite" : item[7], "prix" : item[8], "bid" : item[9], "couverture" : item[10]})
    return render_template("Panier.html", panier=PanierUtilisateur)

@app.route("/PanierRetrait<int:item_id>_<int:boutique_id>_<string:item_type>_<float:item_prix>")
def PanierRetrait(item_id, boutique_id, item_type, item_prix):
    PanierUtilisateur = []
    global ProfilUtilisateur
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd="select quantite from panier where username="+ProfilUtilisateur["username"]+" and lid="+str(item_id)+" and bid="+str(boutique_id)+" and type='"+item_type+"';"
    cur = conn.cursor()
    cur.execute(cmd)
    quantite = cur.fetchone()
    if quantite[0] > 1:
        cmd="update panier set quantite="+str(quantite[0]-1)+" where username="+ProfilUtilisateur["username"]+" and lid="+str(item_id)+" and bid="+str(boutique_id)+" and type='"+item_type+"';"
        cur = conn.cursor()
        cur.execute(cmd)
    else:
        cmd="delete from panier where username="+ProfilUtilisateur["username"]+" and lid="+str(item_id)+" and bid="+str(boutique_id)+" and type='"+item_type+"';"
        cur = conn.cursor()
        cur.execute(cmd)
    cmd='select P.lid, titre, auteur, genre, annee, ville, P.type, P.quantite, P.prix, P.bid, couverture from Catalogue C, Boutiques B, Panier P WHERE P.username='+ProfilUtilisateur["username"]+' and P.lid = C.lid and B.bid = P.bid;'
    cur=conn.cursor()
    cur.execute(cmd)
    cmd='select count(lid) from Panier where username='+ProfilUtilisateur["username"]+';'
    count = conn.cursor()
    count.execute(cmd)
    nb = count.fetchone()
    if nb[0] == 0:
        return render_template("Panier.html", message="Aucun item dans le panier.")
    for i in range(nb[0]):
        item = cur.fetchone()
        PanierUtilisateur.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "ville" : item[5], "type" : item[6], "quantite" : item[7], "prix" : item[8], "bid" : item[9], "couverture" : item[10]})
    return render_template("Panier.html", panier=PanierUtilisateur)

@app.route("/Profil")
def Profil():
    return render_template("Profil.html", profil=ProfilUtilisateur)

@app.route("/ProfilGerant")
def ProfilGerant():
    return render_template("ProfilGerant.html", profil=GerantActif)

@app.route("/InfosBoutique<int:bid>")
def InfosBoutique(bid):
    infos = {}
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='SELECT ville, ventes FROM Boutiques WHERE bid='+str(bid)+';'
    cur=conn.cursor()
    cur.execute(cmd)
    item = cur.fetchone()
    infos["ville"] = item[0]
    infos["ventes"] = item[1]
    return render_template("InfosBoutique.html", infos = infos, gerant = GerantActif)

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

@app.route("/Inventaire<int:bid>")
def Inventaire(bid):
    inventaire = []
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='select I.lid, titre, auteur, genre, annee, type, quantite, prix, couverture from Inventaire I, Catalogue C WHERE I.lid = C.lid and I.bid = '+str(bid)+';'
    cur=conn.cursor()
    cur.execute(cmd)
    cmd='select count(lid) from Inventaire where bid = '+str(bid)+';'
    count = conn.cursor()
    count.execute(cmd)
    nb = count.fetchone()
    if nb[0] == 0:
        return render_template("Inventaire.html", message="Aucun item dans l'inventaire.", gerant=GerantActif)
    for i in range(nb[0]):
        item = cur.fetchone()
        inventaire.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "type" : item[5], "quantite" : item[6], "prix" : item[7], "couverture" : item[8]})
    return render_template("Inventaire.html", inventaire=inventaire, gerant=GerantActif)

@app.route("/InventaireRecherche<int:bid>", methods=['POST'])
def PourRechercheInventaire(bid):
    inventaire = []
    titreLivreRecherche = request.form.get('titreRecherche')
    conn = pymysql.connect(host='localhost', user='root', password='', db='larevel', charset='utf8mb4', autocommit=True)
    cmd = "SELECT I.lid, C.titre, C.auteur, C.genre, C.annee, I.type, I.quantite, I.prix, C.couverture FROM Inventaire I, Catalogue C WHERE I.bid = "+str(bid)+" AND titre LIKE '%" + titreLivreRecherche + "%' AND C.lid = I.lid;"
    cur = conn.cursor()
    cur.execute(cmd)
    infos = cur
    cmd = "SELECT COUNT(C.titre) FROM Catalogue C, Inventaire I WHERE I.bid = "+str(bid)+" AND titre LIKE '%" + titreLivreRecherche + "%' AND C.lid = I.lid;"
    cur = conn.cursor()
    cur.execute(cmd)
    nbTitres = cur.fetchone()
    if nbTitres[0] == 0:
        return render_template("Inventaire.html", inventaire=inventaire, message="Aucun résultat ne correspond à la recherche.", gerant=GerantActif)
    for i in range(nbTitres[0]):
        item = infos.fetchone()
        inventaire.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "type" : item[5], "quantite" : item[6], "prix" : item[7], "couverture" : item[8]})
    return render_template("Inventaire.html", inventaire=inventaire, gerant=GerantActif, nbTitres=nbTitres[0])


@app.route("/Commande")
def Commande():
    global ProfilUtilisateur
    prixTotal = 0
    PanierUtilisateur = []
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='select P.lid, titre, auteur, genre, annee, ville, P.type, P.quantite, P.prix, P.bid, couverture from Catalogue C, Boutiques B, Panier P WHERE P.username='+ProfilUtilisateur["username"]+' and P.lid = C.lid and B.bid = P.bid;'
    cur=conn.cursor()
    cur.execute(cmd)
    cmd='select count(lid) from Panier where username='+ProfilUtilisateur["username"]+';'
    count = conn.cursor()
    count.execute(cmd)
    nb = count.fetchone()
    cmd='select prix, quantite from Panier where username='+ProfilUtilisateur["username"]+';'
    prixEtQuantite = conn.cursor()
    prixEtQuantite.execute(cmd)
    if nb[0] == 0:
        return render_template("Panier.html", rien="Veuillez ajoutez un item à votre panier pour passer une commande.", message="Aucun item dans le panier.")
    for i in range(nb[0]):
        infos = prixEtQuantite.fetchone()
        prixTotal += infos[0] * infos[1]
        item = cur.fetchone()
        PanierUtilisateur.append({"id" : item[0], "titre" : item[1], "auteur" : item[2], "genre" : item[3], "annee" : item[4], "ville" : item[5], "type" : item[6], "quantite" : item[7], "prix" : item[8], "bid" : item[9], "couverture" : item[10]})
    return render_template("Commande.html", commande=PanierUtilisateur, prixTotal=prixTotal)

@app.route("/CommandeConfirmee")
def CommandeConfirmee():
    global ProfilUtilisateur
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd='call updateVentes('+ProfilUtilisateur["username"]+');'
    cur=conn.cursor()
    cur.execute(cmd)
    cmd='select lid, bid, quantite, type from panier where username='+ProfilUtilisateur["username"]+';'
    cur=conn.cursor()
    cur.execute(cmd)
    cmd='select count(lid) from Panier where username='+ProfilUtilisateur["username"]+';'
    count = conn.cursor()
    count.execute(cmd)
    nb = count.fetchone()
    for i in range(nb[0]):
        item = cur.fetchone()
        qty = conn.cursor()
        cmd="select quantite from inventaire where lid="+str(item[0])+" and bid ="+str(item[1])+" and type ='"+item[3]+"';"
        qty.execute(cmd)
        quantite = qty.fetchone()
        if item[2] < quantite[0]:
            update = conn.cursor()
            cmd="update inventaire set quantite=quantite-"+str(item[2])+" where lid="+str(item[0])+" and bid ="+str(item[1])+" and type ='"+item[3]+"';"
            update.execute(cmd)
        else:
            delete = conn.cursor()
            cmd="delete from inventaire where lid="+str(item[0])+" and bid="+str(item[1])+" and type='"+item[3]+"';"
            delete.execute(cmd)
    cmd='delete from panier where username='+ProfilUtilisateur["username"]+';'
    cur=conn.cursor()
    cur.execute(cmd)
    return render_template("CommandeConfirmee.html")

@app.route("/CommandeInventaire")
def CommandeInventaire():
    return render_template("CommandeInventaire.html", gerant=GerantActif)

@app.route("/InventaireAjout<int:bid>", methods=['POST'])
def InventaireAjout(bid):
    titre = '"' + request.form.get('titre') + '"'
    quantite = request.form.get('quantite')
    typeCouverture = '"' + request.form.get('type') + '"'
    prix = request.form.get('prix')
    conn= pymysql.connect(host='localhost',user='root',password='',db='larevel', charset='utf8mb4', autocommit=True)
    cmd="SELECT count(*), I.lid FROM Inventaire I, Catalogue C WHERE C.titre="+titre+" and C.lid = I.lid and I.type="+typeCouverture+" and I.prix="+prix+" and I.bid="+str(bid)+";"
    cur=conn.cursor()
    cur.execute(cmd)
    nb = cur.fetchone()
    if nb[0] == 0:
        cmd='select lid from catalogue where titre='+titre+';'
        cur=conn.cursor()
        cur.execute(cmd)
        lid = cur.fetchone()
        if lid!=None :
            cmd='insert into inventaire value ('+str(lid[0])+','+str(bid)+', '+str(quantite)+', '+typeCouverture+', '+str(prix)+' );'
            cur=conn.cursor()
            cur.execute(cmd)
        else:
            return render_template("CommandeInventaire.html", message="Ce livre ne se retrouve pas dans le catalogue de Larevel.", gerant=GerantActif)
    else:
        cmd="update inventaire set quantite=quantite+"+str(quantite)+" where lid="+str(nb[1])+" and bid ="+str(bid)+" and type ="+typeCouverture+";"
        cur=conn.cursor()
        cur.execute(cmd)
    return render_template("CommandeInventaire.html", message="Commande complétée avec succès! Les exemplaires ont été rajoutés à votre inventaire.", gerant=GerantActif)

if __name__ == "__main__":
    app.run()

