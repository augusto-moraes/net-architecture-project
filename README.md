# net-architecture-project
Network Architecture using GNS3

Ce projet a pour but de créer un réseau MP-BGP/MPLS d'un FAI connecté à plusieurs clients. 
Le nombre de routeur de bordure (PE) du réseau FAI est un critère demandé au début. Un nombre de routeur P du réseau FAI nécessaire va être rajouté automatiquement.
Le nombre de client et de réseau VPN a créer est un critède demandé au début lors de la création.

1er étape -> GNS3_Server_API.py : Connection sur GNS3 sur le serveur local via l'API GNS3:
  Rajout du nombre de routeurs PE et CE voulut ainsi que le nombre de P nécessaire.
  Rajout du nombre de lien entre les routeurs PE et CE. Et PE et P.

2ème étape -> cfg_generator.py : Création des configurations des routeurs
La configuration des routeurs sont prédéfinits suivant 3 catégories :
  - infoPE.json -> Les routeurs PEX : Routeurs de bordure du réseau de coeur. Configuration MP-BGP, OSPF + BGP/MLPS-VPN
  - infoP.json -> Les routeurs PX : Routeurs à l'interrieur du réseau de coeur. Configuration OSPF
  - infoCE.json -> Les routeurs CE-X : Routeurs à l'extérieur du réseau de coeur. Configuration BGP. 

3ème étape -> NOM DE LA FONCTION : Rajout des configurations dans les routeurs via telnet.

## Requirements
* Cisco c7200 ISO
