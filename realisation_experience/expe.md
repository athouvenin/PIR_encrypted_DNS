# Reproduction/Réalisation d’expérience

#### L'expérience choisie correspond à celle décrite dans la partie 3.1 de l'article: SERVERS: TO OFFER DNS-OVER-ENCRYPTION, Discovering open DoT resolvers (page 5)

\
**Objectifs:** 
- retester 1 ou 2 ans plus tard les ip avec port 853 ouvert + répondant aux requêtes DoT
- tenter d'analyser les résultats obtenus et les comparer aux résultats fournis

\
Lien vers les jeux de données et le code source des auteurs de l'article : https://dnsencryption.info/imc19-doe.html

Dans l'article, page 5, nous trouvons l'extrait suivant dans la partie methodologie:

_"In practice, we first use ZMap to discover all IPv4 addresses with port 853 open (using the zmap -p 853 command), and then probe the addresses with DoT queries of a domain registered by us, using getdns API. In the first stage, our scan originates from
3 IP addresses in China and the US (on cloud platforms), and we configure the tool to cover the entire IPv4 address space in a random order. For addresses with port 853 open, only those successfully responding to our DoT queries are regarded as open DoT resolvers."_

C'est donc cette partie de l'expérience que nous allons tenter de réaliser à notre tour. **L'objectif de cette expérience est de rescenser les adresses ip qui répondent aux requêtes DoT.**

\
Pour commencer, j'ai regardé les données et le code source étant à ma disposition (suivre le lien donné plus haut): 

**Partie A** : Open DNS-over-TLS resolvers

Contient les datasets. Nous pouvons tenter de ré-obtenir des jeux de données de ce type en reproduisant l’expérience avec Zmap et getdns, pour une seule requête dans un premier temps, puis pour des ranges  d'addresses ipv4, voir toutes les adresses ipv4.

**Partie B** : ProxyRack source code

Sert à vérifier si les resolvers DNS sont accessibles pour tout le monde (ou sinon pour qui). Le logiciel ProxyRack est payant, donc on abandonne cette partie de l'expérience (pour l’instant au moins).

\
Retour Partie A :
les logiciels à utiliser

- Zmap : network scanning – savoir si le port du DoT (853) est ouvert pour quelle @IP (analyse de réseau)
- getdns : API pour faire des requêtes DoT pour vérif que les @IP avec le port 853 ouvert sont bien capables de répondre aux requêtes DoT.

## Première partie de l'expérience: trouver les ip avec le port 853 ouvert

\
**Le port 853 est le port assigné au DNS-over-TLS (DoT)**. L'intérêt de cette première partie d'expérience est de nous faire gagner beaucoup de temps sur la deuxième partie qui consiste à envoyer des requêtes DoT à des @ip pour voir si elles sont capables d'y répondre.

Le github de Zmap, le wiki est dans l'onglet wiki sur github directement : https://github.com/zmap/zmap

Le github de l'API getdns pour l'installation : https://github.com/getdnsapi/getdns

Une API pour utiliser getdns depuis python directement : https://github.com/getdnsapi/getdns-python-bindings


1. **Installation de Zmap et test avec l’@IP 1.1.1.1 (commande sudo zmap -p 853 1.1.1.1)**

```
$ sudo zmap -p 853 1.1.1.1
[sudo] Mot de passe de agnes : 
Jun 10 16:44:39.310 [WARN] blacklist: ZMap is currently using the default blacklist located at /etc/zmap/blacklist.conf. By default, this blacklist excludes locally scoped networks (e.g. 10.0.0.0/8, 127.0.0.1/8, and 192.168.0.0/16). If you are trying to scan local networks, you can change the default blacklist by editing the default ZMap configuration at /etc/zmap/zmap.conf.
Jun 10 16:44:39.317 [WARN] zmap: too few targets relative to senders, dropping to one sender
Jun 10 16:44:39.318 [INFO] zmap: output module: csv
Jun 10 16:44:39.318 [INFO] csv: no output file selected, will use stdout
 0:00 1%; send: 1 done (20 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 1.1.1.1
 0:01 13%; send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:02 25%; send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:03 38%; send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:04 50%; send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:05 63% (3s left); send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:06 75% (2s left); send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:07 88% (1s left); send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:08 100% (0s left); send: 1 done (20 p/s avg); recv: 1 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
Jun 10 16:44:48.406 [INFO] zmap: completed
```

ça peut mettre un peu de temps à répondre mais au bout de quelque envois, le hitrate passe à 100 %, ça fonctionne !

\
2. **Script python pour générer les adresses ip puis faire le scan avec zmap**

\
Ecriture d'un script (script_ip.py) qui génère les adresses ips et les écrit dans un fichier texte. On pourra ensuite lire ces adresses ip une par une et leur appliquer la commande z-map à l'aide d'un deuxième script.

```
import ipaddress
import os


max_ip = 65536
une_ip = ipaddress.ip_address('0.0.0.0')

with open('all_ips_0.txt', 'w') as f:
    for i in range(0, max_ip):
        
        f.write("%s\n" % item)
        une_ip = une_ip + 1

       

print('finished')
```

le soucis : générer et requeter toutes les adresses ip du monde, ça prend beaucoup de temps !

\
3. **Executer zmap pour des ranges d'ip**

En tapant man z-map dans le terminal, j'ai finalement trouvé dans le manuel d'utilisation un commande que me facilitait la tâche en me fesant tout en un! J'ai donc abandonné ce premier script au profit de la nouvelle commande trouvée.

la commande en question :

```  sudo zmap -p 853 -o test.csv 1.1.1.0/24```

\
En spécifiant le masque (ici /24 par exemple), je spécifie sur quel range d'ip (le nombre d'ip testées à la suite) je veux effectuer mon test. Ci dessous les valeurs correspondantes des masques utilisés:

Mask /24 : 254 ips

Mask /20 : 4094 ips

Mask /19 : 8190 ips

Mask /18 : 16382 ips


```
$ sudo zmap -p 853 -o test.csv 1.1.1.0/24
[sudo] Mot de passe de agnes : 
Jun 10 17:22:04.440 [WARN] blacklist: ZMap is currently using the default blacklist located at /etc/zmap/blacklist.conf. By default, this blacklist excludes locally scoped networks (e.g. 10.0.0.0/8, 127.0.0.1/8, and 192.168.0.0/16). If you are trying to scan local networks, you can change the default blacklist by editing the default ZMap configuration at /etc/zmap/zmap.conf.
Jun 10 17:22:04.450 [INFO] zmap: output module: csv
 0:00 1%; send: 80 0 p/s (1.66 Kp/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:01 13%; send: 256 done (5.04 Kp/s avg); recv: 3 2 p/s (2 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
 0:02 25%; send: 256 done (5.04 Kp/s avg); recv: 3 0 p/s (1 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
 0:03 38%; send: 256 done (5.04 Kp/s avg); recv: 3 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
 0:04 50%; send: 256 done (5.04 Kp/s avg); recv: 3 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
 0:05 63% (4s left); send: 256 done (5.04 Kp/s avg); recv: 3 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
 0:06 75% (3s left); send: 256 done (5.04 Kp/s avg); recv: 3 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
 0:07 88% (2s left); send: 256 done (5.04 Kp/s avg); recv: 3 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
 0:08 100% (0s left); send: 256 done (5.04 Kp/s avg); recv: 3 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 1.17%
Jun 10 17:22:13.502 [INFO] zmap: completed
```

Comme nous le voyons ci-dessus, la durée complete du test prend quelques secondes. Puis nous regardons ce que contient le fichier test.csv:

```
$ cat test.csv
1.1.1.2
1.1.1.1
1.1.1.3
```

Dans le cas testé ci-dessus, 3 @ip sur les 254 testées (entre 1.1.1.1 et 1.1.1.255) ont le port 853 ouvert.

\
En effectuant plusieurs test, je me suis cependant rendu compte que les résultats pouvaient être assez aléatoires. Pour le test réalisé ci-dessus avec 1.1.1.1/24, parfois il y avait zéro ips dans le fichier résultat, parfois seulement 2 sur les 3. Et l'explication de cette irrégularité pourrait s'expliquer par un filtrage de mes requetes par mon FAI. En effet, dans le test effectué, nous voyons que 256 requetes sont envoyées par seconde (et cela peut monter à plusieurs dizaines voir centaines de milier selon la taille du range testé). Ce débit élevé pourrait être détecté comme activité anormale pour mon fai qui filtrerait alors mes requetes. Autre raison, les paquets sont sûrement envoyés avec un protocole UDP pour augmenter la rapidité, mais du coup les paquets peuvent être perdus.

Pour plus de fiabilité, j'ai donc cherché à limiter ce débit; on peut le faire directement dans la commande zmap en ajoutant -r:

Commande z-map avec limitation du débit pour améliorer la fiabilité des résultats:

```sudo zmap -p 853 -r 5 -o test.csv 1.1.1.0/20```

Ici j'ai utilisé -r 5 pour limiter le débit à 5 requetes par secondes (le débit est volontairement pris très faible pour une optimisation maximale)

Si on lance la commande présentée précédement, le test zmap met 14mn à s'executer (pour un masque de 20); ainsi, pour un débit limité à 5 requêtes par secondes et les masques proposés au dessus, les durées de test zmap sont les suivants:

- Pour tester 4094 ips (/20) cela prend 14 mn
- Pour tester 81190 ips (/19) cela prend 28 mn
- Pour tester 16382 ips (/18) cela prend 57 mn

Pour vérifier, je réalise 2 tests pour le range 1.1.1.0/20 avec un débit (rate) limité à 5/s et compare les résultats. Puis j'effectue exactement la même chose sans limiter le débit (cela se fait en quelques secondes contre 2 x 14mn pour le test limitant le débit) et compare à nouveau les résultats. Dans le premier cas, nous obtenons la même chose tandis que dans le deuxième cas, les résultats sont beaucoup plus aléatoires. Je continuerais donc à limiter le débit pour la suite de mon expérience.

\
Suite à celà, je commence à effectuer des tests sur des ranges d'ip un peu aléatoirement: je commence par le range 101.101.101.101/20 (commnade: sudo zmap -p 853 -r 5 -o test101_20.csv 101.101.101.101/20). A la fin du test, mon fichier de sortie test101_20.csv en ressort vide: aucune ip testé n'a le port 853 ouvert.

\
Je décide de passer à un masque /18 (test sur 16382 ips). J'effectue **chaque test 3 fois sur le même range** pour améliorer la qualité de mes résultats. Je concatène ensuite mes 3 fichiers de sortie pour le même range grace à Exel en supprimant les doublons. À ce stade, je suis prête à passer à la deuxième partie de l'expérience: vérifier si les ips récoltées dans le fichier de sortie (qui ont le port 853 ouvert) répondent bien à une requête DoT.

\
J'ai ensuite testé 4 ranges d'ips différentes avec un masque de 20 (tous les résultats sont trouvables dans le dossier test de ce répertoire):

- Test avec 103.205.143.68/18: on trouve 1533 ips différentes avec le port 853 ouvert après les 3 tests (/16382 à priori, ça fait 9,35 %)
- Test avec 176.131.76.200/18: on trouve aucuns résultats (0%)
- Test avec 185.228.168.0/18: on trouve 1064 ips différentes (6,49%)
- Test avec 210.128.97.200: on trouve 6 ips différentes (0,004%)

\
(Pour donner une idée, tester 16382 ip reviens par exemple à tester de l'ip 1.1.0.0 à environ l'ip 1.1.64.0)

Voici comment se présente l'un de ces tests (sur terminal de commande):

```
$ sudo zmap -p 853 -r 5 -o test176_1_18.csv 176.131.76.200/18
[sudo] Mot de passe de agnes : 
Jun 08 09:48:20.470 [WARN] blacklist: ZMap is currently using the default blacklist located at /etc/zmap/blacklist.conf. By default, this blacklist excludes locally scoped networks (e.g. 10.0.0.0/8, 127.0.0.1/8, and 192.168.0.0/16). If you are trying to scan local networks, you can change the default blacklist by editing the default ZMap configuration at /etc/zmap/zmap.conf.
Jun 08 09:48:20.479 [INFO] zmap: output module: csv
 0:00 0%; send: 0 0 p/s (0 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:01 0%; send: 0 0 p/s (0 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:02 0%; send: 6 5 p/s (2 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:03 0%; send: 12 5 p/s (3 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:04 0%; send: 18 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:05 0% (57m left); send: 24 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:06 0% (55m left); send: 30 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:07 0% (1h04m left); send: 30 0 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:08 0% (1h01m left); send: 36 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:09 0% (58m left); send: 42 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:10 0% (57m left); send: 48 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:11 0% (55m left); send: 54 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:12 0% (54m left); send: 60 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:13 0% (59m left); send: 60 0 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:14 0% (58m left); send: 66 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:15 0% (56m left); send: 72 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
```

### **Conclusion et remarques sur cette première partie d'expérience:**

\
Jusque là, je choisi le range plus ou moins au hasard. Mais en fait il y a un peu 2 cas de figure de résultat:

- soit je tombe sur un range ou il y a aucune ip (sur les 16382) avec le port 853 ouvert,
- soit je me positionne là ou je sais qu'il y a des résultats (d'après les données mises à ma disposition par les auteurs de l'article) et je tombe sur des ranges qui sont probablement géré par un même AS (Autonomus System) qui va mettre ses serveurs DNS à la suite, et où les ips avec le port 853 ouvert sont donc toutes concentrées au même endroit et il y a beaucoup de résultats.

Dans tous les cas, c'est vraiment peu représentatif et les tests ne sont pas globaux. De plus, immaginons que je test 6 ranges d'ip de 16382 (ce qui était prévu initialement), cela fait environ 100 000 ip testées sur 4,3 milliards soit une proportion de 2,3 * 10^-5.

Je vais donc commencer par réaliser des requêtes DoT sur ces résultats (2ème partie de l'expérience) puis, suite à ça, je tenterais de trouver un moyen de tester les ips sur un range plus global.


## 2eme partie de l’expérience : envoyer des requetes dot aux adresses ip récupérées dans les scripts

\
En lisant la documentation de getdns, l'API utilisée dans l'expérience originale, je me suis rendue compte qu'elle serait un peu difficile à prendre en main et j'ai cdonc herché quelque chose de plus simple qui pourrait faire la même chose afin de gagner du temps. J'ai donc trouvé une librairie python: **dnspython** qui semblait convenir à l'utilisation dont j'avais besoin.

\
Lien vers la documentation dnspython: https://dnspython.readthedocs.io/en/latest/query.html#tls

### **1ere étape : écrire un script avec la librairie dnspython pour faire une dot query à UNE SEULE @IP**

le script (doT_query.py):

```
import dns.query
import dns.message
import dns.name 

domain = dns.name.from_text('google.com')
mes = dns.message.make_query(domain, dns.rdatatype.A)

try:
    res = dns.query.tls(mes, '1.1.1.6', timeout=2)
    print(res.to_text())
except dns.exception.Timeout:
    print("No answer")
```

\
la réponse lorsque l'on lance le script:

```
si la requête doT est un succès:

id 1059
opcode QUERY
rcode NOERROR
flags QR RD RA
;QUESTION
google.com. IN A
;ANSWER
google.com. 290 IN A 142.250.187.238
;AUTHORITY
;ADDITIONAL

sinon, no answer
```

### **2eme étape : lire les ip du fichier csv et les tester. Stocker le résultat dans la « 2eme colonne » du fichier**

Adaptation du script pour qu'il prenne en argument le fichier d'entrée (contenant les @ip à tester) et le fichier de sortie (contenant ces @ip avec la réponse obtenue à la requête doT):

```
import dns.query
import dns.message
import dns.name 
import csv
import sys

def check_DoT(ip):
    domain = dns.name.from_text('google.com')
    mes = dns.message.make_query(domain, dns.rdatatype.A)

    try:
        res = dns.query.tls(mes, ip, timeout=2) #on laisse 2 secondes à l'ip pour répondre
        return 'respond to DoT query'
        
    except dns.exception.Timeout:
        return 'no answer to DoT query'

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as read_obj:
    with open(output_file, 'w', newline='') as write_obj:
        csv_reader = csv.reader(read_obj)
        csv_writer = csv.writer(write_obj)
        
        for row in csv_reader:
            row.append(check_DoT(row[0]))
            row.append(check_DoT(row[0]))   #on réalise le test 2 fois pour plus de fiabilité dans les résultats
            csv_writer.writerow(row)
```

\
La forme des résultats sur le fichier de sortie (format csv)(test avec le fichier d'entrée test210_1_18.csv):

```
210.128.97.221,respond to DoT query,respond to DoT query
210.128.97.92,respond to DoT query,respond to DoT query
210.128.97.222,respond to DoT query,respond to DoT query
210.128.97.89,respond to DoT query,respond to DoT query
210.128.97.91,respond to DoT query,respond to DoT query
210.128.97.219,respond to DoT query,respond to DoT query
```

Remarque: certaines @ip bloquaient le script et généraient des erreurs car elles fesait partie de la blacklist (voir la "capture terminal ci-après); j'ai donc levé une deuxième exception dans le script afin de résoudre ce problème.

```
$ python3 doT_query.py tout103.csv res103_doT.csv
Traceback (most recent call last):
  File "doT_query.py", line 34, in <module>
    row.append(check_DoT(row[0]))
  File "doT_query.py", line 16, in check_DoT
    res = dns.query.tls(mes, ip, timeout=2) #on laisse 2 secondes à l'ip pour répondre
  File "/home/agnes/.local/lib/python3.8/site-packages/dns/query.py", line 809, in tls
    _tls_handshake(s, expiration)
  File "/home/agnes/.local/lib/python3.8/site-packages/dns/query.py", line 737, in _tls_handshake
    s.do_handshake()
  File "/usr/lib/python3.8/ssl.py", line 1304, in do_handshake
    self._check_connected()
  File "/usr/lib/python3.8/ssl.py", line 1088, in _check_connected
    self.getpeername()
OSError: [Errno 107] Transport endpoint is not connected
 ```

Et voici alors le script doT_query.py modifié en conséquence:

```
import dns.query
import dns.message
import dns.name 
import csv
import sys



def check_DoT(ip):
    domain = dns.name.from_text('google.com')
    mes = dns.message.make_query(domain, dns.rdatatype.A)

    try:
        res = dns.query.tls(mes, ip, timeout=2) #on laisse 2 secondes à l'ip pour répondre
        return 'DoT query answer'
        
    except dns.exception.Timeout:
        return 'DoT query timeout'

    except:
        return 'DoT query error'
        


input_file = sys.argv[1]
output_file = sys.argv[2]


with open(input_file, 'r') as read_obj:
    with open(output_file, 'w', newline='') as write_obj:
        csv_reader = csv.reader(read_obj)
        csv_writer = csv.writer(write_obj)
        
        for row in csv_reader:
            row.append(check_DoT(row[0]))
            row.append(check_DoT(row[0]))   #on réalise le test 2 fois pour plus de fiabilité dans les résultats
            csv_writer.writerow(row)
```

### **4ème étape: appliquer le script doT_query à chaque échantillon relevé concaténer**

Résultats: (fichier de la forme res103_doT.csv)

- Test avec les résultats de 103.205.143.68/18: aucune @ip/1533 ne répond
- Test avec les résultats de 185.228.168.0/18: 1021 réponses /1063 (96%)
- Test avec les résultats de 210.128.97.200: 6 réponses /6 (100%)

\
Nous conclueront sur ces résultats une fois que nous aurons également les résultats avec des tests plus globaux et représentatifs.

## 3ème partie: chercher à réaliser des tests sur des ranges plus globaux et représentifs

### *1ère possibilité* : tester toutes les @ip en fesant un saut de x @ip entre chaque ip testé

Tester 100 000 @ip en limitant le débit à 5 requêtes/seconde devrait prendre environ 5h30. Je décide donc de tester environs 100 000 réparties sur la totalité du range des adresses ipv4. 

La totalité des @ip = 4,3 x 10⁹

4,3 x 10⁹/40 000 = 107 000 donc on va tester une @ip toutes les 40 000.

\
On a la possibilité avec zmap de lire un fichier d’entrée avec la commande : --whitelist-file. Cela se présente comme ceci:

```
sudo zmap -p 853 --whitelist-file tout210.csv
Jun 13 21:28:39.898 [WARN] zmap: too few targets relative to senders, dropping to one sender
Jun 13 21:28:39.899 [INFO] zmap: output module: csv
Jun 13 21:28:39.899 [INFO] csv: no output file selected, will use stdout
 0:00 1%; send: 6 done (108 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
210.128.97.92
210.128.97.89
210.128.97.91
210.128.97.222
210.128.97.221
210.128.97.219
 0:01 13%; send: 6 done (108 p/s avg); recv: 6 5 p/s (5 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:02 26%; send: 6 done (108 p/s avg); recv: 6 0 p/s (2 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:03 38%; send: 6 done (108 p/s avg); recv: 6 0 p/s (1 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:04 50%; send: 6 done (108 p/s avg); recv: 6 0 p/s (1 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:05 63% (3s left); send: 6 done (108 p/s avg); recv: 6 0 p/s (1 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:06 75% (2s left); send: 6 done (108 p/s avg); recv: 6 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:07 88% (1s left); send: 6 done (108 p/s avg); recv: 6 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
 0:08 101% (0s left); send: 6 done (108 p/s avg); recv: 6 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 100.00%
Jun 13 21:28:49.003 [INFO] zmap: completed
```

\
On reprend alors le script python (script_ip) que l’on a fait initialement qui générait les adresses ip dans un fichier, on le modifie pour qu'il fasse des sauts de 40 000 ip à chaque itération puis on donnera ce fichier à zmap.

```
import ipaddress
import os


max_ip = 107374 # (2^32 / 40000, car on fait une ip toutes les 40 000)
une_ip = ipaddress.ip_address('0.0.0.0')

with open('all_ips_40.txt', 'w') as f:
    for i in range(0, max_ip):
        
        f.write("%s\n" % une_ip)
        une_ip = une_ip + 40000

       

print('finished')
```

\
on lance la commande zmap :

```
[1]> sudo zmap -p 853 -r5 --whitelist-file all_ips_40.txt -o test_all40.csv 
Jun 13 20:11:37.149 [INFO] zmap: output module: csv
 0:00 0%; send: 0 0 p/s (0 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:01 0%; send: 4 3 p/s (3 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:02 0%; send: 9 4 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:03 0%; send: 14 4 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:04 0%; send: 20 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:05 0% (5h25m left); send: 24 3 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:06 0% (5h11m left); send: 30 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:07 0% (5h20m left); send: 34 3 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:08 0% (5h10m left); send: 40 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:09 0% (5h17m left); send: 44 3 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:10 0% (5h10m left); send: 50 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:11 0% (5h15m left); send: 54 3 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
 0:12 0% (5h10m left); send: 60 5 p/s (4 p/s avg); recv: 0 0 p/s (0 p/s avg); drops: 0 p/s (0 p/s avg); hitrate: 0.00%
```

\
Cette possibilité testant 107 000 @ip prend environ 5h20 à s'executeur. Une fois fait, le fichier de résultats contients seulement **75 @ip avec le port 853 ouvert**. On envoie ensuite des requêtes DoT à ces résultats de la même manière que précédement et **aucune ip ne répond (0%)**.

### *2ème possibilité* : tester toutes les ips du monde sans limiter le débit :

Avec cette possibilité qui envoie des centaines de milliers de requêtes /seconde, d'une part la box internet est très sollicité et donc beaucoup de paquets seront perdues, et j'effectue ce teste en connassance de cause. Mais il apparait pour moi comme un bon moyen de tester des @ip de manière vraiment aléatoire en couvrant toute l'amplitudes des adresses ipv4.

J'utilise donc simplement la commande qui suit et attends qu'elle aie fini de s'executer; cela prend un peu moins de 3h.

```sudo zmap -p 853  -o test_all1.csv 0.0.0.0/0```

\
**Nous obtenons 1454 résultats**, donc 1454 @ip avec le port 853 ouvert. Nous appliquons ensuite les requêtes DoT à ces résultats, toujours de la même façon que précédement et nous avons **5 réponses, soit 0,0034%**.

\
**Conclusion sur les réponses aux requêtes DoT des @ips avec le port 853 ouvert:**  **[A COMPLETER]**, dans l'article c'est dit

Parmis les tests faits, surtout les derniers qui sont un peu plus représentatifs, nous observons très peu de résultats, que ce soit pour le nombre d'@ip avec le port 853 ouvert et encore plus le nombre d'@ip qui répondent aux requêtes DoT. C'était plutôt attendu, et ces résultats sont cohérents avec ce qui a été présenté dans l'article de référence. (On rappelle que d'après l'article moins de 1% des requêtes DNS du monde sont chiffrées).

Cependant, nous avons bien des résultats "positifs", dans le sens où nous avons trouvé des hosts qui répondent aux requêtes DoT, ce qui prouvent bien que ces serveurs DoT sont présents et existent vraiment.

En outre, nous pouvons remarquer qu'il y a quand même beaucoup de host (ou d'@ip) qui ne répondent pas aux requêtes DoT alors qu'elles ont le port 853 ouvert. Nous pouvons alors nous demander pourquoi, et quels peuvent être les autres utilisation de ce port?

Tout d'abord, le port 853 est contenu dans le range des ports normés, c'est à dire des ports spécifiques réservé à une utilité, en l'occurence à écouter le traffic Dot pour le port 853. Les raisons qui pourraient alors expliquer pourquoi les hosts ont le port 853 ouvert mais ne répondent pas aux requêtes DoT peuvent être parce que le serveur à qui ont effectue la requête filtre mes requêtes, par exemple parce que l'ip de ma machine n'appartient pas à un range d'ip autorisé par le serveur. Cela peut aussi être une erreur du coté du serveur, soit parce qu'il reçoit trop de straffic, soit à cause d'un problème de configuration. Enfin, il est également possible que le port 853 du serveur soit ouvert pour une autre utilisation, à ce moment spécifique à ce serveur, et configuré manuellement comme tel, auquel cas il ne peut pas répondre aux requêtes DoT.

---------------------

From each Internet-
wide scan, we discover 2 to 3 million hosts with port 853 open (e.g.,
356M on Feb 1 and 230M on May 1), yet a vast majority of them
do not provide DoT (i.e., they cause getdns errors). ~0,06 % d'après l'article (1,5 K / 2,5 M)