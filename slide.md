---
title: Jenkins
theme: slide
paginate: true
footer: Paul Lion
header: Simplon
marp: true
size: 16:9
---

# 1. Introduction.
**Jenkins.**
**Azure.**
**Python.**
*Mise en place par Paul et Quentin.*

---
# Sommaire
* 1 Introduction.
* 2 Missions.
* 3 Objectifs.
* 4 Ressouces.
* 5 Déploiment de l'infrastructure.
* 6 Installation de l'application et ses dépendances.
* 7 Retrospective du sprint.


---
# 2. Mission.
Bonjour,
Tu as bien travaillé pour le Nextcloud de Lifesense, merci !
J'ai regardé les demandes de déploiements d'applications et j'ai remarqué qu'il y a beaucoup de tickets qui
concernent ces 3 applications : Nextcloud, Gitea et Jenkins.
On pourrait gagner beaucoup de temps à les automatiser !
Est-ce que tu peux en choisir une et préparer un script de déploiement complètement automatisé ?
Je compte sur toi.
Cordialement,
Le chef

---
# 3. Objectifs.
# 3.1 Managements.
* Présenté votre travail
* Pratiqué Scrum
* Abordé la gestion de projet
* Abordé la communication en équipe
* Mieux anticipé vos actions que dans le brief précédent

---
# 3. Objectifs.
# 3.1 Techniques.
* Déployé de nouvelles ressources dans Azure
* Implémenté des scripts
* Utilisé un bastion
* Mis en place un moyen de surveillance de la disponibilité de l'application
* Configuré la rétention des logs
* Parsé du JSON
* Utilisé certbot pour déployer un certificat TLS

---
# 3. Topologie infrastructure.
![](./IMG/infra.png)

---
# 4. Ressources.
* Un groupe de ressource azure.
* Un réseau. (10.0.1.0/24)
* Deux sous-réseaux. (Bastion: 10.0.1.0/26 App: 10.0.1.64/26)
* Deux ip publiques.
* Deux groupes de sécurité.
* Une machine virtuelle.

---
# 5. Déploiment de l'infrastructure.
## 5.1 Outils:
* Utilisation de Python.
* Utlisation d'Azure CLI.

---
# 5. Déploiment de l'infrastructure.
## 5.2 Organisation du code:
* Fonctions
* Main process

---
# 5. Déploiment de l'infrastructure.
## 5.3 Difficultés:
* Installation de bastion.
* Activation du tunnel sur bastion.
* Utilisation du tunnel pour envoyer le script bash sur la VM
* Modification des fichier de configuration en utilisant bash


---
# 6. Installation de l'application et ses dépendances
## 6.1 Outils:
* Python.
* Nginx.
* Jenkins.

---
# 6. Installation de l'application et ses dépendances
## 6.2 Organisation du code:
* Fonction.
* Main process
* insertion du script bash dans une fonction "connect_bastion'

---
# 6. Installation de l'application et ses dépendances
## 6.3 Difficultés:
* paramétrage de la redirection (proxy_pass) de nginx pour permettre l'accès à jenkins

---
<!-- _backgroundColor: #282a36 -->
<!-- _color: #f8f8f2 -->
# 7. Reste à réaliser :
* Définir les utilisateurs (adminstration vm et administrateur jenkins
* Finaliser l'installation de jenkins en ligne de commande (activation de jenkins.cli)
* Optimiser le script pour récupérer les informations nécessaire à l'établissement d'un rapport sur les ressources déployées
* mettre en place le TSL de jenkins
* récupération des logs
* mettre en place le backup préconnisé
---
# Utilisation du script
* Il est possible de paramétrer les noms du groupe de ressource et celui de la VM (Ces noms seront utilisés pour définir les noms des autres ressources qui leurs sont attachées.

---
<<<<<<< HEAD
# 7 Retrospective du sprint.
# 7.1 Qu'est ce qui c'est bien passé ?
=======
# 9 Retrospective de sprint.
# 9.1 Qu'est ce qui c'est bien passé ?
>>>>>>> 5434f50 (Update slide.md)
* On a bien échangé sur les différents problémes que l'on a rencontré.
* On a partagé et on s'est soutenu tout le long du projet.
* On a travaillé ensemble sur la partie deploiment de l'infrastructure et sur le début de la rédaction du projet.

<<<<<<< HEAD
---
# 7 Retrospective du sprint.
# 2. Qu'est ce qui ne c'est pas bien passé ?
* On a fais le projet chacun de notre coté, on n'a pas assez travaillé ensemble. Du coup on a perdu beaucoup de temps alors que si on avait étè plus collaboratif on aurait pu tout faire et bien plus.
=======
# 9.2 Qu'est ce qui ne c'est pas bien passé ?
* On a fais le projet chacun de notre coté, on n'a pas assez travaillé ensemble. Du coup on a perdu beaucoup de temps alors que si on avait été plus collaboratif, on aurait pu tout faire et bien plus.
>>>>>>> 5434f50 (Update slide.md)
* Répartition des taches. Il était difficile de répartir les taches car tout le monde voulait tout voir pour pouvoir apprendre.
* Sur la partie deploiment de l'application nous avons utilisé des stratégies différentes ce qui a rendu la collaboration difficile.
* Scrum: Néccésité d'avoir le même scrum master tout le long du processus pour coordonner les tâches, le timming, la communication dans le groupe, définir la stratégie adoptée et les technologies à utiliser
