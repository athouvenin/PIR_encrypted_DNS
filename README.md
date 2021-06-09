# PIR sur le DNS encrypté
#### Le PIR (Projet d'Initiation à la Recherche) est un projet de recherche sur un sujet en particulier réalisé dans le cadre de la 3ème année d'études à l'INSA (département Télécommunications). Le sujet de mon PIR au sens large est intitulé "DNS et vie privée" (voir descriptif ci-dessous). 

Descriptif du sujet: Le trafic DNS n’est pas protégé comme peut l’être le reste du trafic sur Internet avec
des protocoles comme TLS. Cependant, les identifiants contenu dans les requêtes et réponses DNS
peuvent révéler des informations sur les sites visites par les utilisateurs. Ces informations peuvent
être exploitées pour mettre en place une surveillance des utilisateurs ou pour censurer certains
contenus. Plusieurs initiatives récentes vises à protéger le contenu du trafic DNS et sont en cours de
déploiement a grande échelle._

Plus précisément, je me suis penchée sur le déploiement récent et actuel du DNS encrypté à grande échelle en me basant sur l'article de recherche: **"An End-to-End,
Large-Scale Measurement of DNS-over-Encryption: How Far Have We Come?"** . Ce document date de octobre 2019  et contient une étude du sujet au cours de cette même année, il y alors deux ans.

(référence de l'article: Chaoyi Lu, Baojun Liu, Zhou Li, Shuang Hao, Haixin Duan, Mingming Zhang,
Chunying Leng, Ying Liu, Zaifeng Zhang, and Jianping Wu. 2019. An End-to-End,
Large-Scale Measurement of DNS-over-Encryption: How Far Have We Come?.
In IMC '19: Proceedings of the Internet Measurement Conference 2019. ACM, New
York, NY, USA, 14)

Mon étude s'est déroulée en plusieurs parties:

- dans un premier temps, un travail sur l'article de référence et la réalisation d'une synthèse de celui-ci
- dans un deuxième temps, une étude des expériences réalisées dans l'article afin d'apporter une dimension pratique au projet

Suite à celà, j'ai choisi l'une des expériences décrite dans l'article pour en analyser ses résultats et essayer de la reproduire au mieux pour pouvoir exploiter des résultats plus actuels. A noter que les auteurs de l'article ont également rendu disponible toutes leurs données facilitant grandement leur exploitation et la reproduction d'expérience.

Le travail expérimentale s'est donc fait sur plusieurs axes:

- une partie sur l'**analyse des données fournies**
- une partie orientée sur la **réalisation et la reproduction d'expérience** puis analyse des résultats trouvées
- _idéalement une partie sur la comparaison des résultats de l'articles et des miens_
