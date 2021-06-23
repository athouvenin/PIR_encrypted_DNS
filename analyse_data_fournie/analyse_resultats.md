# Analyse des données fournies par les auteurs et comparaison avec les résultats présentés dans l'article

### L'objectif est de vérifier les résultats présentés dans l'article, et entre autre ceux présentés dans le tableau 2 (le nombre de resolvers doT par pays). j'ai donc analysé avec Exel 3 jeux de données proposés: celui du 01/02/2019, celui du 01/05/2019 et celui du 01/07/2020. Pour ces trois jeux de données, j'ai évalué le nombre de resolvers doT par pays, la proportion par pays des resolveurs qui contenaient un certificat ssl 'ok' et finalement quels était les noms de domaines qui revenaient le plus (via un tableur + un graphe pour chaque thématique). 

\
Lien vers les jeux de données et le code source des auteurs de l'article : https://dnsencryption.info/imc19-doe.html

Ces jeux de données correspondent aux résultats des @IP du monde qui répondent aux requêtes DoT.
\
Remarque: Vous trouverez ce jeux de données ainsi que leur analyses dans les fichiers au format xlsx (Exel) de ce répertoire.

Autre remarque: les jeux de données ne contiennent que des réponses aux requêtes DoT, nous nous concentrerons donc uniquement sur ce protocole pour les analyses et les expériences.

\
**Préambule**: que contient ces jeux de données? Comment sont ils organisés?  

Ces jeux de données sont organisés dans des fichiers définis par la date du test auquel ils ont été effectué. Ils se présentent comme suit:

![](./captures/apercu_web.png)

\
Chaque colonne peut s'identifier comment suit (avec Domaine pour le nom de domaine, et certificat valide pour la validité du certificat ssl, dont le rôle est expliqué dans le fichier synthèse_article.md):

![](./captures/aperçu_tableur.png)


Les fichiers dataset sont téléchargés enregistrés en texte document puis ouvert avec exel. Puis j'ai fait des observations des diverses résultats en réalisant des tableaux croisés dynamiques puis des graphes croisés dynamiques (outils Exels, je vous invite à aller consulter mes fichiers qui sont joints dans ce dossier).

Pour chaque jeu de données (j'en ai analysé 3), 4 évaluations ont été faites:

- 1) le nombre de résolveurs répondant aux DoT queries dans le monde
- 2) le nombre de resolveurs en question que possède chaque pays
- 3) la proportion de certificat ssl 'ok'
- 4) le nombre de résolveurs pour chaque Nom de Domaine (Common Name)

### 1) le nombre de résolveurs répondant aux DoT queries dans le monde

\
**Dataset du 01/02/2019** : 1198

\
**Dataset du 01/05/2019** : 2053

\
**Dataset du 01/07/2020** : 7062

\
**Observations / Remarques / Conclusion**

Nous trouvons quelques milliers de résolveurs qui répondent au DoT D'abord, les résultats de 2019 collent avec ceux annoncé dans l'article. Effectivement, à la fin de la page 5 il est écrit "As shown in Figure 3, **over 1.5K open DoT resolvers are discovered** in each scan, significantly more than the public resolver lists".

Par ailleurs, nous constatons l'augmentation du nombre avec le temps, notament entre l'année 2019 et 2020, ce qui est encore un fois conforme avec ce que propose l'article.

### 2) le nombre de resolveurs en question que possède chaque pays

\
**Dataset du 01/02/2019**

48 pays dans le monde contiennent au moins un résolveur de DoT.

\
**Dataset du 01/05/2019**

55 pays dans le monde contiennent au moins un résolveur de DoT.

\
**Comparaison avec le tableau**

![](./captures/Tableau2.png)

Voici le tableau que l'on peut trouver dans l'article, page 5. En analysant avec Exel les datasets concernés par le tableau (février et mai 2019) je trouve : 

![Top 15 des pays avec le plus de résolveurs DoT en février 2019](./captures/tab_nb_pays02.PNG) 

***Top 15 des pays avec le plus de résolveurs DoT en février 2019***

![Top 15 des pays avec le plus de résolveurs DoT en mai 2019](./captures/tab_nb_pays05.PNG)

***Top 15 des pays avec le plus de résolveurs DoT en mai 2019***

En comparant, on retrouve globalement les mêmes valeurs, c'est donc cohérent.

\
**Dataset du 01/07/2020**

52 pays dans le monde contiennent au moins un résolveur de DoT.

Comme pour les deux datasets précédents, voici le top 15 des pays contenant le plus de résolveur DoT

![Top 15 des pays avec le plus de résolveurs DoT en juillet 2020](./captures/tab_nb_pays07.PNG)

\
On remarque l'absence de l'irelande dans ce nouveau top, alors qu'il était le grand leader en 2019 sur les différents datasets étudiés. Apart ce résultat, on retrouve les mêmes pays que précédement, même si le classement est un peu modifié.

\
**Observations / Remarques / Conclusion**

### 3) la proportion de certificat ssl 'ok'

\
**Dataset du 01/02/2019**

Proportion moyenne des certificats ssl valides (j'ai comptabilisé les 'ok'): 91%

Et les résultats de cette proportion par pays est représentée sur le graphe qui suit: (les pays sont ordonnées de manière décroissantes par rapport au nombre de résolveurs DoT qu'ils possèdent)

![](./captures/gra_pc_ok02.png)

\
**Dataset du 01/05/2019**

Proportion moyenne des certificats ssl valides: 91%

Et les résultats de cette proportion par pays est représentée sur le graphe qui suit: (les pays sont ordonnées de manière décroissantes par rapport au nombre de résolveurs DoT qu'ils possèdent)

![](./captures/gra_pc_ok05.png)

\
**Dataset du 01/07/2020**

Proportion moyenne des certificats ssl valides: 77,4%

Et les résultats de cette proportion par pays est représentée sur le graphe qui suit: (les pays sont ordonnées de manière décroissantes par rapport au nombre de résolveurs DoT qu'ils possèdent)

![](./captures/gra_pc_ok07.png)

\
**Observations / Remarques / Conclusion**

### 4) le nombre de résolveurs pour chaque Nom de Domaine (Common Name)

\
**Dataset du 01/02/2019**

\
1196 résultats (noms différents en enlevant les erreurs).
On filtre les 10 premiers pour avoir un camembert lisible. Les plus grosses parts :
    1 CN=*.cleanbrowsing.org (Domaine)
    2 - : Pas de nom de domaine 



Cleanbrowsing : 40%
Autres (<14 itérations, représentent chacun 1% ou moins individuellement) : 32%
Pas de CN : 23%
Cloudflare : 3%
Dns.iij.jp : 2%

\
**Dataset du 01/05/2019**

\
**Dataset du 01/07/2020**

\
**Observations / Remarques / Conclusion**

**Dataset du 01/02/2019**
