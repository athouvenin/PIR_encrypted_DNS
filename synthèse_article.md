# An End-to-End, Large-Scale Measurement of DNS-over-Encryption: How Far Have We Come? (Oct 2019)


### Problématique : Où en est le deploiement et l'utilisation du DNS chiffré ?


Le DNS est aujourd’hui présent dans presque toutes l’activité d’Internet : pour envoyer des mails (consultation de serveurs d’adresses), pour faire des requêtes de nom de domaine ; même les appareils (devices) utilisent DNS pour se découvrir l’un l’autre. Par son implémentation traditionnelle, les paquets DNS sont envoyés sans aucune encryption, rendant ces paquets vulnérables à des attaques de diverses natures.

Et en effet, il a récement été mis en lumière la réalité des choses, à savoir l’exploitation de cette vulnérabilité dans le designe du DNS, compromettant la sécurité et la vie privée des utilisateurs d’Internet. Parmi les risques auxquels ces utilisateurs sont exposés, on retrouve : des machines clientes pouvant être traquées à travers Internet seulement en analysant leur données relatives au traffic DNS. Outre la surveillance, les « attaques » peuvent aller au-delà en altérant, traffiquant, censurant un partie du traffic. Pour résumer, on se rend compte que le traffic DNS non protégé peut entrainer de sérieux problèmes d’exposition et d’exploitation de la vie privée des utilasateurs d’Internet.

C’est pourquoi, pour pallier à ce problème, plusieurs protocols ont été proposés pour encrypter les requêtes DNS entre les clients et les serveurs, que nous généraliseront par l’appellation DNS-over-Encryption (DoE). Parmis ces protocoles, nous retrouvons DNS-over-TLS (DoT), DNS-over-HTTPS(DoH), DNS-over-QUIC et DNSCrypt. L’efficacité de ces protocoles sera étudiée et comparée dans le document.
Le but de cet article est en fait de faire un état lieu (où nous en sommes) du DNS encrypté à grande échelles. Et ce en s’appuyant sur les thèmes/questions suivantes :

1. **Combien de fournisseurs offrent un service de DNS-over-Encryption (DoE) ? Est-ce que leur implémentation est sécurisée ?**
2. ***Y a-il des différences de performances pour l’utilisateur ? Y a-il des problème d’accès ou des erreurs causées à cause du DoE ?***
3. _Aujourd’hui (fin 2019), concrètement, quelle est l’utilisation réelle du DoE à grande échelle ?_

Pour les chiffres, il est annoncé plus de 150 fournisseurs pour DoT et 17 pour DoH qui offrent un service de DNS-over-Encryption. Fin 2019, le volume de traffic de DoE reste petit par rapport au DNS traditionnel, malgré une hausse dans les derniers mois. Par exemple, Cloudflare DoT témoigne une augmentation de 56 % du trafic entre Juillet et Décemebre 2018.

Jusque là, les résultats montrent que la qualité du service fourni par le DoE est efficace et satisfesante en générale, malgré l’observation d’une légère hausse de latence en utilisant DoE. Cependant, il a été relevé des erreurs de configuration dans certains services ce qui cause des erreurs. D’autre part, ils se sont rendu compte qu’une part importante fournisseurs utilisaient des certificats SSL invalides ce qui risque de ruiner le processus d’autentification du serveur. 

Pour conclure, les DoE et notament les protocols  DNS-over-TLS et  DNS-over-HTTPS sont une solution prometteuse pour résoudre les problème rencontrés par le trafic DNS non encrypté. Cependant, pour que cela puisse fonctionner au mieux, des efforts doivent être faits de la part des fournisseurs pour proposer une implémentation révisée pour qu’elle soit correcte et éviter les erreurs. Une généralisation à grande échelle de cette implémentation encryptée est finalement  largement recommandée et encouragée par les auteurs de l’article.

#### Définitions/Vocabulaire supplémentaire

DoE : DNS-over-Encryption

TLS : Transport Layer Security

SSL : Security Socket Layer

Transport Layer Security (TLS), and its now-deprecated predecessor, Secure Sockets Layer (SSL), are cryptographic protocols designed to provide communications security over a computer network (wikipedia)