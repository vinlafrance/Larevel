import pymysql.cursors

connection = pymysql.connect(
    host="localhost",
    user="root",
    password=,
    db="",
    autocommit=True)

cursor = connection.cursor()

creation_table = "CREATE TABLE IF NOT EXISTS Clients(username varchar(100), password varchar(100), nom varchar(100), adresse varchar(100), PRIMARY KEY(username));" \
"CREATE TABLE IF NOT EXISTS Gerants(gid integer, nom varchar(100), PRIMARY KEY(gid));" \
"CREATE TABLE IF NOT EXISTS Boutiques(bid integer, ville varchar(100), gid integer, PRIMARY KEY(bid), FOREIGN KEY(gid) REFERENCES (Gerants));" \
"CREATE TABLE IF NOT EXISTS Inventaire(lid integer, bid integer, quantite integer, type varchar(10), prix double," \
"FOREIGN KEY(lid) REFERENCES (Catalogue), FOREIGN KEY(bid) REFERENCES (Boutiques));" \
"CREATE TABLE IF NOT EXISTS Catalogue(lid integer AUTO_INCREMENT, titre varchar(100), auteur varchar(100), genre varchar(100), annee year, PRIMARY KEY(lid));" \
"CREATE TABLE IF NOT EXISTS Panier(username varchar(100), lid integer, bid integer, quantite integer, type varchar(10), prix double," \
"FOREIGN KEY(username) REFERENCES (Clients), FOREIGN KEY(lid) REFERENCES (Catalogue), FOREIGN KEY(bid) REFERENCES (Boutiques));"

cursor.execute(creation_table)


