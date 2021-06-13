# SYNTHÈSE: An End-to-End, Large-Scale Measurement of DNS-over-Encryption: How Far Have We Come? (Oct 2019)


### Problématique : Où en est le deploiement et l'utilisation du DNS chiffré ?


Le DNS (Domaine Name System) est aujourd’hui indispensable et omniprésent dans l’utilisation d’internet. En effet, une requête DNS se résoud en traduisant une url lisible pour l’utilisateur en adresse IP permettant de localiser le serveur hébergent la page web ou le service en quelques milisecondes à peine. Cependant, par son implémentation traditionnelle, les paquets DNS sont envoyés sans aucune encryption, rendant ces paquets vulnérables (à de la surveillance du traffic DNS, de la censure, de la manipulation des réponses DNS, de la redirection de traffic), nuisant à la sécurité et la vie privée des utilisateurs d’Internet.

\
C’est pourquoi, pour pallier à ce problème, des solutions ont été déployées depuis quelques années et plusieurs protocoles ont été proposés pour chiffrer les requêtes DNS entre les clients et les serveurs, que nous généralisont par l’appellation DNS chiffré (ou DoE pour DNS-over-Encryption). Parmis eux nous retrouveront notamment DoT (DNS-over-TLS), encryptant les requêtes DNS au niveau de la couche de transport (protocols TCP/UDP) et DoH (DNS-over-HTTPS), encryptant cette fois- ci les requêtes au niveau de la couche application (protocole HTTPS). L’efficacité des protocoles chiffrés fait d'ailleurs l'objet d'une des études menées au cours de l'article. 

\
Le but de cet article, **An End-to-End, Large-Scale Measurement of DNS-over-Encryption: How Far Have We Come?** est en fait de faire un état lieu (où nous en sommes) du DNS encrypté à grande échelles. Et ce en s’appuyant sur les thèmes/questions suivantes :

1. Combien de fournisseurs offrent un service de DNS-over-Encryption (DoE) ? Est-ce que leur implémentation est sécurisée ?
2. Y a-il des différences de performances pour l’utilisateur ? Y a-il des problème d’accès ou des erreurs causées à cause du DoE ?
3. Aujourd’hui (fin 2019), concrètement, quelle est l’utilisation réelle du DoE à grande échelle ?

Pour les chiffres, il est annoncé plus de 150 fournisseurs pour DoT et 17 pour DoH qui offrent un service de DNS-over-Encryption. Fin 2019, le volume de traffic de DoE reste petit par rapport au DNS traditionnel, malgré une hausse dans les derniers mois. Par exemple, Cloudflare DoT témoigne une augmentation de 56 % du trafic entre Juillet et Décemebre 2018.

Jusque là, les résultats montrent que la qualité du service fourni par le DoE est efficace et satisfesante en générale, malgré l’observation d’une légère hausse de latence en utilisant DoE. Cependant, il a été relevé des erreurs de configuration dans certains services ce qui cause des erreurs. D’autre part, ils se sont rendu compte qu’une part importante fournisseurs utilisaient des certificats SSL invalides ce qui risque de ruiner le processus d’autentification du serveur. 

Pour conclure, les DoE et notament les protocols  DNS-over-TLS et  DNS-over-HTTPS sont une solution prometteuse pour résoudre les problème rencontrés par le trafic DNS non encrypté. Cependant, pour que cela puisse fonctionner au mieux, des efforts doivent être faits de la part des fournisseurs pour proposer une implémentation révisée pour qu’elle soit correcte et éviter les erreurs. Une généralisation à grande échelle de cette implémentation encryptée est finalement  largement recommandée et encouragée par les auteurs de l’article.

\
**Définitions/Vocabulaire supplémentaire**

DoE : DNS-over-Encryption

TLS : Transport Layer Security

SSL : Security Socket Layer

Transport Layer Security (TLS), and its now-deprecated predecessor, Secure Sockets Layer (SSL), are cryptographic protocols designed to provide communications security over a computer network (wikipedia)


## Certificats SSL invalides, pourquoi ?

https://sematext.com/blog/ssl-certificate-error/?fbclid=IwAR1TcZga8Ff880WIlN56SM--kZ5PkxQHvcpDejlE9laxlMu2S0yGYL0Cxo8
https://sectigostore.com/page/solve-the-invalid-ssl-tls-certificate-issue/?fbclid=IwAR2gG_7_85lCqnArZj9MXCJge2eWDwvjl6Lb20czgDIZrH86ZTHG86CKSqA

SSL certificates are data files hosted by the server that makes the SSL encryption possible. They contain the server’s public key and identity

SSL helps to keep sensitive information like usernames, passwords, credit cards, etc. secure by encrypting the data between the client and the server. You need SSL for three reasons: privacy, integrity, and identification.
An SSL certificate helps a browser verify the identity of a website. By using the SSL certificates, the browser can ensure that it is connected to the exact website the user intended to. SSL certificates guarantee that you are the legitimate and verified owner of the website.

Needless to say, you should always stay on top of any SSL error messages you or your site visitors may receive errors concerning your website certificate.

Types of SSL Certificate Errors: Causes & How to Fix Them 

    • 1. Expired Certificate 

    • 2. Inactive Certificate 

    • 3. Certificate lifetime greater than 398 days 

    • 4. Missing Hostname 

    • 5. Invalid/Incomplete Certificate Chain 

    • 6. Revoked Certificate 

    • 7. Untrusted Certificate Authority 

    • 8. Insecure Signature Algorithm 

    • 9. Missing/Incorrect Certificate Transparency Information

There can be a few reasons why the browser decides to flash the invalid SSL certificate error message on our screens. Below, we take a look at some of these and explore ways to fix them.

    • If the website owner misconfigures the SSL certificate during installation, there is no way to access the HTTPS version correctly. Every time someone accesses the website, their browser will flash this error on the screen.

    • Invalid SSL certificate / Intermediate certificates error could occur when as a website owner, you are trying to install the certificate on your web server or CDN, but the relevant certificate details are not filled correctly. You can use the free SSL Checker from Qualys SSL Labs to check if the SSL certificate has been configured correctly on the web server.

    • The certificate has been revoked or was obtained illegally.

    • ERR_CERT_COMMON_NAME_INVALID error indicates there is a possible mismatch in names of the domain you are trying to access and the one included in the certificate. The website owner must confirm the web address in the correct format before the CA issues the certificate. Remember that the domain https://www.example.com might be included in the certificate while https://example.com is different and might not be registered as a part of the SSL certificate.

    • The certificate’s chain of trust is broken (could be because the root CA can’t be verified, or the root/intermediate certificate has expired). 

    • The certificate must be renewed before the expiry of the certificate to avoid any conflict arising out of time violation. Ensure that the date/time is set correctly on your computer since that might be used to assess the validity period of the SSL certificate of the website.

    • The certificate structure is broken, or the certificate’s signature can’t be checked.

    • It is preferred to obtain a certificate from trusted Certificate Authorities (CA) like Symantec, Thawte, Comodo, etc. to avoid any security warnings from browsers. If a self-signed certificate is being used, configure the domain to use Full SSL instead of Full SSL (Strict).

    • Check the antivirus or firewall. You might need to disable any option like “encrypted/SSL scanning or checking.”

    • Websites using only SHA-1 encryption are flagged as insecure and need to update their security certificates. 