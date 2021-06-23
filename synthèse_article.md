# SYNTHÈSE SUR L’ARTICLE : An End-to-End, Large-Scale Measurement of DNS-over-Encryption: How Far Have We Come? (Oct 2019)


### Problématique : Où en est le déploiement et l’utilisation du DNS chiffré ? Est-ce une solution utilisée à grande échelle ?


Le DNS (Domaine Name System) est aujourd’hui indispensable et omniprésent dans l’utilisation d’internet. En effet, une requête DNS se résout en traduisant une URL lisible et compréhensible pour l’utilisateur en une adresse IP permettant de localiser le serveur hébergent la page web ou le service en quelques millisecondes à peine. Cependant, par son implémentation traditionnelle, les paquets DNS sont envoyés sans être protégés, rendant ces paquets vulnérables (à de la surveillance du trafic DNS, de la censure, de la manipulation des réponses DNS, de la redirection de trafic), nuisant à la sécurité et la vie privée des utilisateurs d’Internet.

\
C’est pourquoi, pour pallier à ce problème, des solutions ont été déployées depuis quelques années et plusieurs protocoles ont été proposés pour chiffrer les requêtes DNS entre les clients et les serveurs, que nous généralisons par l’appellation DNS chiffré (ou DoE pour DNS-over-Encryption). Parmi eux nous retrouverons notamment DoT (DNS-over-TLS), encapsulant les requêtes DNS au niveau de la couche Transport (protocole TCP/UDP) et DoH (DNS-over-HTTPS), encapsulant cette fois-ci les requêtes au niveau de la couche Application (protocole HTTPS). L’efficacité des protocoles chiffrés est d'ailleurs l'un des objets d'étude dont les résultats sont présentés dans l'article.

\
Le but de cet article, **An End-to-End, Large-Scale Measurement of DNS-over-Encryption: How Far Have We Come?** est en fait de faire un état lieu (où nous en sommes) du DNS chiffré à grande échelle. Et ce en s’appuyant sur les thèmes/questions suivantes :

1. Combien de fournisseurs offrent un service de DNS-over-Encryption (DoE) ? Est-ce que leur implémentation est sécurisée ?
2. Y a-t-il des différences de performances pour l’utilisateur ? Y a-t-il des problèmes d’accès ou des erreurs causées à cause du DoE ?
3. Aujourd’hui (fin 2019), concrètement, quelle est l’utilisation réelle du DoE à grande échelle ?

Pour les chiffres, il est annoncé plus de 150 fournisseurs pour DoT et 17 pour DoH qui offrent un service de DNS-over-Encryption. Fin 2019, le volume de trafic de DoE reste très très petit par rapport au DNS traditionnel : (moins de 1 % des résolveurs de DNS publics sont capables de répondre à une requête DoT). Malgré tout, on observe une hausse du trafic DoE ces derniers temps ; par exemple, Cloudflare DoT témoigne une augmentation de 56 % du trafic entre juillet et décembre 2018.

Jusque-là, les résultats montrent que la qualité du service fourni par le DoE est efficace et satisfaisante en général, malgré l’observation d’une légère hausse de latence (peu significative) en utilisant DoE. Cependant, il a été relevé des problèmes de configuration dans certains services ce qui cause des erreurs. D’autre part, ils se sont rendu compte qu’une part importante fournisseurs utilisaient des certificats SSL invalides ce qui pouvait empêcher que le processus d’authentification du serveur se fasse.

Pour conclure, d’après l’article, les DoE et notament les protocols DNS-over-TLS et DNS-over-HTTPS sont une solution prometteuse pour résoudre les problèmes rencontrés par le trafic DNS non chiffré. Cependant, pour que cela puisse fonctionner au mieux, des efforts doivent être faits de la part des fournisseurs pour proposer une implémentation révisée pour qu’elle soit correcte et éviter les erreurs. Une généralisation à grande échelle de cette solution est finalement largement recommandée et encouragée par les auteurs de l’article.


## Définitions/Vocabulaire supplémentaire

DoE : DNS-over-Encryption

TLS : Transport Layer Security

SSL : Security Socket Layer

Transport Layer Security (TLS), and its now-deprecated predecessor, Secure Sockets Layer (SSL), are cryptographic protocols designed to provide communications security over a computer network (wikipedia)


## Complément d’information : Certificats SSL, que sont ils et pourquoi peuvent ils être invalides ?

https://sematext.com/blog/ssl-certificate-error/?fbclid=IwAR1TcZga8Ff880WIlN56SM--kZ5PkxQHvcpDejlE9laxlMu2S0yGYL0Cxo8
https://sectigostore.com/page/solve-the-invalid-ssl-tls-certificate-issue/?fbclid=IwAR2gG_7_85lCqnArZj9MXCJge2eWDwvjl6Lb20czgDIZrH86ZTHG86CKSqA

Les certificats SSL sont des fichiers de données stockés par les serveurs et qui permettent le chiffrement des connexions. Ils contiennent la clé publique du serveur et son identité.

SSL aide à maintenir sécurisé les informations sensibles tel que les noms d’utilisateurs, les mots de passes, les numéros de cartes bancaires, etc., en chiffrant les données entre le client et le serveur. Les certificats SSL sont nécessaires pour trois besoins : la confidentialité, l’intégrité et l’identification.
Un certificat SSL aide un navigateur à vérifier l’identité d’un site Internet. En utilisant les certificats SSL, le navigateur s’assure qu’il est connecté au site souhaité par l’utilisateur. Les certificats SSL garantissent que vous êtes le propriétaire légitime du site.

Il est inutile de préciser que vous ne devez par avoir d’erreur SSL sur votre site, sinon les visiteurs recevront des erreurs concernant le certificat de votre site.

Types d’erreurs des certificats SSL

    • 1. Certificat expiré

    • 2. Certificat inactif 

    • 3. Durée de vie du certificat excédant 398 jours

    • 4. Domaine manquant

    • 5. Impossible de valider la chaîne de certificats 

    • 6. Certificat révoqué

    • 7. CA (Certificate Authority) non fiable

    • 8. Algorithme de signature non sécurisé

    • 9. Impossible de valider les informations de transparence

Il existe plusieurs raisons qui amènent le navigateur à marquer un certificat SSL comme invalide et afficher un message d’erreur sur l’écran. Ci-dessous, nous verrons quelques-unes comment les corriger certaines des erreurs précédentes :

    • Si le propriétaire du site configure de la mauvaise manière le certificat SSL durant l’installation, il n’existe aucun moyen d’accéder à la version HTTPS du site correctement. Chaque fois qu’un utilisateur accède au site, le navigateur affichera une erreur.

    • Les erreurs de certificats invalides peuvent arriver quand, en tant que propriétaire du site, vous essayer d’installer un certificat sur votre serveur web ou CDN, mais que les détails de celui-ci ne sont pas renseignés correctement. Dans ce cas, vous pouvez utiliser le vérificateur SSL de Qualys SSL pour vérifier la bonne configuration.

    • L’erreur ERR_CERT_COMMON_NAME_INVALID indique qu’il existe une incohérence entre le nom de domaine auquel vous essayez d’accéder et celui inclus dans le certificat. Le propriétaire du site doit confirmer l’URL de son site dans le bon format avant que le CA fournisse un certificat. Souvenez-vous que le domaine https://www.example.com est différent du domaine https://example.com et n’est pas forcément enregistré dans le certificat SSL.

    • La chaîne de certificats est invalide par exemple, si le CA racine ne peut pas être vérifié ou si un certificat intermédiaire a expiré.

    • Le certificat doit être renouvelé avant la date d’expiration pour éviter tout conflit qui se manifesterait après cette date. Assurez-vous que l’heure et la date de votre ordinateur est correcte car elle pourrait servir à confirmer la période de validité du certificat SSL. 

    • Il est préférable d’obtenir un certificat provenant d’un CA de confiance tel que like Symantec, Thawte, Comodo, etc., afin d’éviter tout avertissement de sécurité affiché par le navigateur. Si un certificat auto-signés est utilisé, configurez le domaine pour qu’il utilise Full SSL au lieu de Full SSL (strict).

    • Vérifiez que votre antivirus ou votre pare-feu, les options tel que « scan SSL ou vérifications » peuvent être à désactiver.
    
    • Les sites utilisant seulement un chiffrement SHA-1 sont marqués comme non sécurisés et doivent mettre à jour leurs certificats de sécurité.
