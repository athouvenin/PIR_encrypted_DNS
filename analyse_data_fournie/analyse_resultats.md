# Analyse des données fournies par les auteurs et comparaison avec les résultats présentés dans l'article

### L'objectif est de vérifier les résultats présentés dans l'article, et entre autre ceux présentés dans le tableau 2 (le nombre de resolvers doT par pays). j'ai donc analysé avec Exel 3 jeux de données proposés: celui du 01/02/2019, celui du 01/05/2019 et celui du 01/07/2020. Pour ces trois jeux de données, j'ai évalué le nombre de resolvers doT par pays, la proportion par pays des resolveurs qui contenaient un certificat ssl 'ok' et finalement quels était les noms de domaines qui revenaient le plus (via un tableur + un graphe pour chaque thématique). 

\
Lien vers les jeux de données et le code source des auteurs de l'article : https://dnsencryption.info/imc19-doe.html

\
Remarque: Vous trouverez ce jeux de données ainsi que leur analyses dans les fichiers au format xlsx (Exel) de ce répertoire.

\
**Préambule**: que contient ces jeux de données? Comment sont ils organisés?  **[A COMPLETER]**


Fichier dataset téléchargé enregistré en texte document puis ouvert avec exel. Observations des diverses résultats en réalisant des tableaux croisés dynamiques puis des graphes croisés dynamiques (outils Exels, je vous invite à aller consulter mes fichiers qui sont joints dans ce dossier).

Pour chaque jeu de données, 4 évaluations ont été faites:

- 1) le nombre de résolveurs répondant aux DoT queries dans le monde
- 2) le nombre de resolveurs en question que possède chaque pays
- 3) la proportion de certificat ssl 'ok'
- 4) le nombre de résolveurs pour chaque Nom de Domaine (Common Name)

### 1) le nombre de résolveurs répondant aux DoT queries dans le monde

\
**Dataset du 01/02/2019**


\
**Dataset du 01/05/2019**

\
**Dataset du 01/07/2020**

\
**Observations / Remarques / Conclusion**

### 2) le nombre de resolveurs en question que possède chaque pays

\
**Dataset du 01/02/2019**

\
Open DoT resolvers dans 37 pays différents ; 1198 open dot resolvers e tout (compter 1198 @ip différentes).
Comparaison avec le tableau donné dans l’article :

Globalement, pour chaque chiffre du tableau, il y en a quelques-uns en plus par rapport aux résultats trouvés dans le dataset.

\
**Dataset du 01/05/2019**

\
**Dataset du 01/07/2020**

\
**Observations / Remarques / Conclusion**

### 3) la proportion de certificat ssl 'ok'

\
**Dataset du 01/02/2019**

\
**Dataset du 01/05/2019**

\
**Dataset du 01/07/2020**

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
