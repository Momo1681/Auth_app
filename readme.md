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
FONT TT T 
- Des le lancement du programme un superuser est cree avec l'email: root@root.net, et le mot de passe: password
- Aussi apres le lancement du processus les utilisateurs sont appelle a creer un superuser
- Les utilisateur creer ont pour mot de passe password qu'il faudra changer 