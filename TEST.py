import sqlite3

#Connexion
connexion = sqlite3.connect('mabasecobaye.db')

#Récupération d'un curseur
c = connexion.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS table(
    Id INT,
    Nom TEXT,
    Mdp TEXT,
    Score INT);
    """)
Id = 0
Nom = ''
Mdp = ''
Score = 0


p = "INSERT INTO table VALUES ('" + Id + "','" + Nom + "','" + Mdp + "','" + Score + "')"

c.executescript(p)

#Validation
connexion.commit()

#Déconnexion
connexion.close()