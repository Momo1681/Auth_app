import os
import sqlite3
import hashlib

"""
- Nom du systeme : systeme d'authentification en ligne de commande ecrite en python
- Le langage est : python. Durant notre parcours universitaire, on a eu a etudier le langage de programmation python notament pour mettre en place des application distribuer dans un reseau
- Lien Github:
- Membre du groupe:

PROPOSITION
- L'idee de ce systeme est de permettre d'authentifier des utilisateurs en vue qu'il accede a des fonctionnalites ou des traitemant particlier(Les traitements metier n'ont pas ete deleloppe)
- Carasteristique:
    ** Creation des utilisateurs avec un nom, prenom, email, et un type(Gestionnaire, client, superuser) et un mot de passe hashe
    ** Connexion a partie de la ligne de commande, avec un email et un mot de passe
    ** Toutes les donnees sont stockes dans une base de donnee sqlite3
- Elements de securite
    ** L'authentification
    ** L'autorisation
    ** Confidentialite
- Des le lancement du processus, les utilisateurs sont appeles a se connecter avec leurs email et leur mot de passe, une fois loger les utilisateurs peuvent se deconnecter et changer leur mot de passe a tout moment
- Oui
"""
# Création de la table des utilisateurs
"""c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nom TEXT NOT NULL,
              prenom TEXT NOT NULL,
              email TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL,
              type TEXT NOT NULL)''')"""

# Vérifier si la base de données existe déjà
if not os.path.exists("users.db"):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Créer la table users
    c.execute('''CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                username TEXT NULL,
                prenom TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                type TEXT NOT NULL
                )''')

    # Créer le superutilisateur
    print("Ceux-ci est la premiere execution du programme, Veuillez creer un superuser :)")
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    email = input("Email: ")
    username = input("Nom d'utilisateur: ")
    password = input("PASSWD : ")
    # Vérifier si l'utilisateur existe déjà
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    if c.fetchone():
        print("Un utilisateur avec cet email existe déjà.")
    else:
        # Créer un nouveau mot de passe aléatoire
        password = hashlib.sha256(password.encode()).hexdigest()
        # Ajouter l'utilisateur à la base de données
        c.execute("INSERT INTO users (nom, username, prenom, email, password, type) VALUES (?, ?, ?, ?, ?, ?)",
                  (nom, username, prenom, email, password, "superuser"))
        conn.commit()
        print("Superutilisateur créé avec succès.")
else:
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

# Demander à l'utilisateur de se connecter
while True:
    print("Veuillez vous connecte")
    email = input("Email: ")
    password = input("Mot de passe: ")
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email, hashlib.sha256(password.encode()).hexdigest()))
    user = c.fetchone()
    if user:
        current_user = {"id": user[0], "nom": user[1], "username": user[2], "prenom": user[3], "email": user[4],
                        "type": user[6]}
        print(f"Bienvenue, {current_user.get('prenom')} {current_user.get('nom')} ({current_user.get('type')})")
        break
    else:
        print("Email ou mot de passe incorrect.")


def create_user():
    # Vérifier si l'utilisateur est un gestionnaire ou un superutilisateur
    """if current_user.get("type") not in ["gestionnaire", "superuser"]:
        print("Seuls les gestionnaires et les superutilisateurs peuvent créer des utilisateurs.")
        return"""
    # Demander les informations de l'utilisateur
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    email = input("Email: ")
    # Vérifier si l'utilisateur existe déjà
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    if c.fetchone():
        print("Un utilisateur avec cet email existe déjà.")
        return
    # Créer un nouveau mot de passe aléatoire
    password = hashlib.sha256("password".encode()).hexdigest()
    # Ajouter l'utilisateur à la base de données
    c.execute("INSERT INTO users (nom, prenom, email, password, type) VALUES (?, ?, ?, ?, ?)",
              (nom, prenom, email, password, "client"))
    conn.commit()
    print("Utilisateur créé avec succès.")

# Fonction pour se connecter
def login():
    # Demander l'email et le mot de passe
    email = input("Email: ")
    password = input("Mot de passe: ")
    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email, hashlib.sha256(password.encode()).hexdigest()))
    user = c.fetchone()
    if user:
        # Connecter l'utilisateur
        global current_user
        current_user = {"id": user[0], "nom": user[1], "prenom": user[2], "email": user[3], "type": user[5]}
        print("Connecté en tant que", current_user["type"])
    else:
        print("Email ou mot de passe incorrect.")


# Fonction pour se déconnecter
def logout():
    global current_user
    current_user = None
    print("Déconnecté.")


# Fonction pour afficher les informations d'un utilisateur
def view_user():
    # Vérifier si l'utilisateur est connecté
    if not current_user:
        print("Vous devez être connecté.")
        return
    # Demander l'email de l'utilisateur à afficher
    email = input("Email de l'utilisateur: ")
    # Vérifier si l'utilisateur existe
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    if user:
        print("Nom:", user[1])
        print("Prénom:", user[2])
        print("Email:", user[3])
        print("Type:", user[5])
    else:
        print("Cet utilisateur n'existe pas.")


# Fonction pour afficher le menu
def menu():
    print("0. Afficher le menu")
    print("1. Créer un nouvel utilisateur")
    print("2. Se connecter")
    print("3. Se déconnecter")
    print("4. Afficher la liste des utilisateurs")
    print("5. Supprimer un utilisateur")
    print("6. Modifier le mot de passe")
    print("7. Info Utilisateur")
    print("8. Quitte")

# Fonction pour afficher la liste des utilisateurs
def list_users():
    # Vérifier si l'utilisateur est un gestionnaire ou un superutilisateur
    """if current_user.get("type") not in ["gestionnaire", "superuser"]:
        print("Seuls les gestionnaires et les superutilisateurs peuvent afficher la liste des utilisateurs.")
        return"""
    # Afficher la liste des utilisateurs
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    if users:
        for user in users:
            print("Non", "Prenom", "Email")
            print(user[1], user[2], "-", user[3], "-", user[5])
    else:
        print("Aucun utilisateur.")


# Fonction pour supprimer un utilisateur
def delete_user():
    # Vérifier si l'utilisateur est un gestionnaire ou un superutilisateur
    if current_user.get("type") not in ["gestionnaire", "superuser"]:
        print("Seuls les gestionnaires et les superutilisateurs peuvent supprimer des utilisateurs.")
        return
    # Demander l'email de l'utilisateur à supprimer
    email = input("Email de l'utilisateur à supprimer: ")
    # Vérifier si l'utilisateur existe
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    if user:
        # Supprimer l'utilisateur
        c.execute("DELETE FROM users WHERE email=?", (email,))
        conn.commit()
        print("Utilisateur supprimé avec succès.")
    else:
        print("Cet utilisateur n'existe pas.")


# Fonction pour modifier le mot de passe d'un utilisateur
def change_password():
    # Vérifier si l'utilisateur est connecté
    if not current_user:
        print("Vous devez être connecté.")
        return
    # Demander l'ancien et le nouveau mot de passe
    old_password = input("Ancien mot de passe: ")
    new_password = input("Nouveau mot de passe: ")
    # Vérifier si l'ancien mot de passe est correct
    c.execute("SELECT * FROM users WHERE id=? AND password=?",
              (current_user.get("id"), hashlib.sha256(old_password.encode()).hexdigest()))
    user = c.fetchone()
    if user:
        # Modifier le mot de passe
        c.execute("UPDATE users SET password=? WHERE id=?",
                  (hashlib.sha256(new_password.encode()).hexdigest(), current_user.get("id")))
        conn.commit()
        print("Mot de passe modifié avec succès.")
    else:
        print("Mot de passe incorrect.")

# Fonction pour quitter le programme 2/3/6/7/1/==>4/5
def quit_program():
    global execution
    execution = False
    print("À bientôt !")


# Utilisateur en cours de connexion
current_user = None

# Création du superutilisateur
c.execute("SELECT * FROM users WHERE email=?", ("root@root.net",))
user = c.fetchone()
if not user:
    c.execute("INSERT INTO users (nom, prenom, email, password, type) VALUES (?, ?, ?, ?, ?)",
              ("Super", "User", "root@root.net", hashlib.sha256("password".encode()).hexdigest(), "superuser"))
    conn.commit()
    print("Superutilisateur créé avec succès.")

# Boucle principale du programme
execution = True
while execution:
    print("0. Afficher le menu")
    print("1. Créer un nouvel utilisateur")
    print("2. Se connecter")
    print("3. Se déconnecter")
    print("4. Afficher la liste des utilisateurs")
    print("5. Supprimer un utilisateur")
    print("6. Modifier le mot de passe")
    print("7. Info User")
    print("8. Quitter")

    choice = input("Entrez votre choix: ")
    if choice == "0":
        menu()
    elif choice == "1":
        create_user()
    elif choice == "2":
        login()
    elif choice == "3":
        logout()
    elif choice == "4":
        list_users()
    elif choice == "5":
        delete_user()
    elif choice == "6":
        change_password()
    elif choice == "7":
        view_user()
    elif choice == "8":
        quit_program()
    else:
        print("Choix invalide.")


