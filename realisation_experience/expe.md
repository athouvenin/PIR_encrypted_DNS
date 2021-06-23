# Reproduction/Réalisation d’expérience

#### l'expérience choisie correspond à celle décrite dans la partie 3.1 de l'article: SERVERS: TO OFFER DNS-OVER-ENCRYPTION, Discovering open DoT resolvers (page 5)

\
**Objectifs:**
- retester 1 ou 2 ans plus tard les adresses IPavec port 853 ouvert + répondant aux requêtes DoT
- tenter d’analyser les résultats obtenus et les comparer aux résultats fournis (car les jeux de données disponibles correspondent aux résultats des @IPdu monde qui répondent aux requêtes DoT)

\
Lien vers les jeux de données et le code source des auteurs de l’article : https://dnsencryption.info/imc19-doe.html

Dans l'article à la section "3.1 Methodology", page 5, nous trouvons l'extrait suivant :

_"In practice, we first use ZMap to discover all IPv4 addresses with port 853 open (using the zmap -p 853 command), and then probe the addresses with DoT queries of a domain registered by us, using getdns API. In the first stage, our scan originates from
3 IPaddresses in China and the US (on cloud platforms), and we configure the tool to cover the entire IPv4 address space in a random order. For addresses with port 853 open, only those successfully responding to our DoT queries are regarded as open DoT resolvers."_

C'est donc cette partie de l'expérience que nous allons tenter de réaliser à notre tour. **l'objectif de cette expérience est de recenser les adresses IP qui répondent aux requêtes DoT.**

\
Pour commencer, j'ai regardé les données et le code source étant à ma disposition (suivre le lien donné plus haut) :

**Partie A** : Open DNS-over-TLS resolvers

Contiens les jeu de données. Nous pouvons tenter de ré-obtenir des jeux de données de ce type en reproduisant l'expérience avec Zmap et getdns, pour une seule requête dans un premier temps, puis pour des plages d'addresses IPv4, voir toutes les adresses IPv4.

**Partie B** : ProxyRack source code

Sers à vérifier si les résolveurs DNS sont accessibles pour tout le monde (ou sinon pour qui). Le logiciel ProxyRack est payant, donc on abandonne cette partie de l'expérience (pour l'instant au moins).

\
Retour Partie A :
les logiciels à utiliser

- Zmap : scanner réseau – savoir si le port du DoT (853) est ouvert pour quelle @IP (analyse de réseau)
- getdns : API pour faire des requêtes DoT pour vérifier que les @IP avec le port 853 ouvert sont bien capables de répondre aux requêtes DoT.

## Première partie de l'expérience: trouver les IP avec le port 853 ouvert

\
**Le port 853 est le port assigné au DNS-over-TLS (DoT)**. l'intérêt de cette première partie d'expérience est de nous faire gagner beaucoup de temps sur la deuxième partie qui consiste à envoyer des requêtes DoT à des @IP pour voir si elles sont capables d'y répondre.

Le github de Zmap (le wiki est dans l'onglet wiki sur github directement) : https://github.com/zmap/zmap

Le github de l'API getdns pour l'installation : https://github.com/getdnsapi/getdns

Une API pour utiliser getdns depuis python directement : https://github.com/getdnsapi/getdns-python-bindings


1. **Installation de Zmap puis test avec l'@IP 1.1.1.1 (commande sudo zmap -p 853 1.1.1.1)**

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

ça peut mettre un peu de temps à répondre mais au bout de quelques envois, le hitrate passe à 100 % (comme on peut le voir sur la capture du terminal), ça fonctionne !

\
2. **Script python pour générer les adresses IP puis faire le scan avec zmap**

\
Écriture d'un script (script_ip.py) qui génère les adresses IP et les écrit dans un fichier texte. On pourra ensuite lire ces adresses IP une par une et leur appliquer la commande zmap à l'aide d'un deuxième script.

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

les soucis : générer et requêter toutes les adresses IP du monde, ça prend beaucoup de temps !

\
3. **Exécuter zmap pour des plages d'IP**

En tapant man zmap dans le terminal, j'ai finalement trouvé dans le manuel d'utilisation une commande que me facilitait la tâche en me faisant tout en un ! J'ai donc abandonné ce premier script au profit de la nouvelle commande trouvée.

la commande en question :

```  sudo zmap -p 853 -o test.csv 1.1.1.0/24```

\
En spécifiant le masque (ici /24 par exemple), je spécifie sur quelle plage d'IP (le nombre d'IP testées à la suite) je veux effectuer mon test. Je n'ai donc plus besoin de générer dans un fichier le range d'adresse IP à tester, et seules les adresses avec le port 853 ouvert seront écrites dans le fichier de sortie (appelé test.csv dans la commande d'exemple ci-dessus).

 Ci-dessous les valeurs correspondantes des masques utilisés :

- Mask /24 : 254 ips
- Mask /20 : 4094 ips
- Mask /19 : 8190 ips
- Mask /18 : 16382 ips

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

Comme nous le voyons ci-dessus, la durée complète du test prend quelques secondes. Puis nous regardons ce que contient le fichier de sortie test.csv:

```
$ cat test.csv
1.1.1.2
1.1.1.1
1.1.1.3
```

Dans le cas testé ci-dessus, 3 @IP sur les 254 testées (entre 1.1.1.1 et 1.1.1.255) ont le port 853 ouvert.

\
En effectuant plusieurs tests, je me suis cependant rendu compte que les résultats pouvaient être assez aléatoires. Par exemple pour le test réalisé ci-dessus avec 1.1.1.1/24, parfois il y avait zéro IP dans le fichier résultat, parfois seulement 2 sur les 3. Et cette irrégularité pourrait s'expliquer par un filtrage de mes requêtes par mon FAI. En effet, dans le test effectué, nous voyons que 256 requêtes sont envoyées par seconde (et cela peut monter à plusieurs dizaines voir centaines de milliers selon la taille de la plage testée). Ce débit élevé pourrait être détecté comme activité anormale pour mon FAI qui filtrerait alors mes requêtes. Autre raison, les paquets sont sûrement envoyés avec un protocole UDP pour augmenter la vitesse d'exécution, mais du coup les paquets peuvent être perdus.

Pour plus de fiabilité, j'ai donc cherché à limiter ce débit; on peut le faire directement dans la commande zmap en ajoutant -r:

Commande zmap avec limitation du débit pour améliorer la fiabilité des résultats:

```sudo zmap -p 853 -r 5 -o test.csv 1.1.1.0/20```

Ici j'ai utilisé -r 5 pour limiter le débit à 5 requêtes par secondes (le débit est volontairement pris très faible pour une optimisation maximale).

Si on lance la commande présentée précédemment, le test zmap met 14mn à s’exécuter (pour un masque de 20); ainsi, pour un débit limité à 5 requêtes par secondes et les masques proposés au-dessus, les durées de test zmap sont les suivants :

- Pour tester 4094 IP (/20) cela prend 14 mn
- Pour tester 81190 IP (/19) cela prend 28 mn
- Pour tester 16382 IP (/18) cela prend 57 mn

Pour vérifier, je réalise 2 tests pour la plage 1.1.1.0/20 avec un débit (rate) limité à 5/s. Puis j'effectue exactement la même chose sans limiter le débit (cela se fait en quelques secondes contre 2 x 14mn pour le test limitant le débit. Je compare ensuite les résultats des différents tests. Dans le premier cas, nous obtenons la même chose tandis que dans le deuxième cas, les résultats sont beaucoup plus aléatoires. Je continuerais donc à limiter le débit pour la suite de mon expérience.

\
Suite à cela, je commence à effectuer des tests sur des plages d'IP un peu aléatoirement: je commence par la plage 101.101.101.101/20 (commnade: sudo zmap -p 853 -r 5 -o test101_20.csv 101.101.101.101/20). A la fin du test, mon fichier de sortie test101_20.csv en ressort vide: aucune IP testée n'a le port 853 ouvert.

\
Je décide de passer à un masque /18 (test sur 16382 IP). J'effectue **chaque test 3 fois sur le même range** pour améliorer la qualité de mes résultats. Je concatène ensuite mes 3 fichiers de sortie pour le même range grâce à Excel en supprimant les doublons. Une fois que j'aurais testé plusieurs range d'IP comme décrit juste avant, je serais prête à passer à la deuxième partie de l'expérience: vérifier si les IP récoltées dans le fichier de sortie (qui ont le port 853 ouvert) répondent bien à une requête DoT.

\
J'ai donc testé 4 plages d'IP différentes avec un masque de 18 (tous les fichiers de résultats sont trouvables dans le dossier "TESTS" de ce répertoire):

- Test avec 103.205.143.68/18: on trouve 1533 IP différentes avec le port 853 ouvert après les 3 tests (/16382 à priori, ça fait 9,35 %)
- Test avec 176.131.76.200/18: on trouve aucuns résultats (0%)
- Test avec 185.228.168.0/18: on trouve 1064 IP différentes (6,49%)
- Test avec 210.128.97.200: on trouve 6 IP différentes (0,004%)

\
(Pour donner une idée, tester 16382 IP reviens par exemple à tester de l'IP 1.1.0.0 à environ l'IP 1.1.64.0)

Voici comment se présente l'un de ces tests (aperçu du terminal de commande):

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

Jusque-là, je choisissais la plage plus ou moins au hasard. Mais en fait il y a un peu 2 cas de figure de résultats :

- soit je tombe sur un range ou il y a aucune IP (sur les 16382) avec le port 853 ouvert,
- soit je me positionne là ou je sais qu'il y a des résultats (d'après les données mises à ma disposition par les auteurs de l'article) et je tombe sur des plages qui sont probablement gérées par un même AS (Autonomus System) qui va mettre ses serveurs DNS à la suite, et où les IP avec le port 853 ouvert sont donc toutes concentrées au même endroit et il y a beaucoup de résultats.

Dans tous les cas, c'est vraiment pas représentatif et les tests ne sont pas globaux (sur la totalité de "l'amplitude" des adresses IP). De plus, imaginons que je teste 6 plages d'IP de 16382 (ce qui était prévu initialement), cela fait environ 100 000 IP testées sur 4,3 milliards soit une proportion de 2,3 * 10^-5.

Je vais donc commencer par réaliser des requêtes DoT sur ces résultats (2ème partie de l'expérience) puis, suite à ça, je tenterais de trouver un moyen de tester les IP sur une plage plus globale.


## 2eme partie de l'expérience : envoyer des requêtes DoT aux adresses IP récupérées dans les scripts

\
En lisant la documentation de getdns, l'API utilisée dans l'expérience originale, je me suis rendue compte qu'elle serait un peu difficile à prendre en main en peu de temps et j'ai donc cherché quelque chose de plus simple qui pourrait faire la même chose afin de gagner du temps. J'ai trouvé une librairie python: **dnspython** qui semblait convenir à l'utilisation dont j'avais besoin.

\
Lien vers la documentation dnspython: https://dnspython.readthedocs.io/en/latest/query.html#tls

### **1ere étape : écrire un script avec la librairie dnspython pour faire une reqête DoT à UNE SEULE @IP**

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

### **2eme étape : lire les IP du fichier csv et les tester. Stocker le résultat dans la « 2eme colonne » du fichier**

Adaptation du script pour qu'il prenne en argument le fichier d'entrée (contenant les @IP à tester) et le fichier de sortie (contenant ces @IP avec la réponse obtenue à la requête doT):

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
        res = dns.query.tls(mes, ip, timeout=2) #on laisse 2 secondes à l'IP pour répondre
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

Remarque: certaines @IP bloquaient le script et généraient des erreurs car elles fesait partie de la blacklist (voir la "capture terminal" ci-après); j'ai donc levé une deuxième exception dans le script afin de résoudre ce problème.

```
$ python3 doT_query.py tout103.csv res103_doT.csv
Traceback (most recent call last):
  File "doT_query.py", line 34, in <module>
    row.append(check_DoT(row[0]))
  File "doT_query.py", line 16, in check_DoT
    res = dns.query.tls(mes, ip, timeout=2) #on laisse 2 secondes à l'IP pour répondre
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
        res = dns.query.tls(mes, ip, timeout=2) #on laisse 2 secondes à l'IP pour répondre
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

### **4ème étape: appliquer le script doT_query.py à chaque échantillon relevé avec le port 853 ouvert (échantillons concaténés au préalable)**

Résultats: (fichier de la forme res103_doT.csv)

- Test avec les résultats de 103.205.143.68/18: aucune @ip/1533 ne répond
- Test avec les résultats de 185.228.168.0/18: 1021 réponses /1063 (96%)
- Test avec les résultats de 210.128.97.200: 6 réponses /6 (100%)

Remarque: Pour rappel, avec le set de 176.131.76.200/18 nous n'avions aucune IP avec le port DoT ouvert, donc ce n'est pas la peine d'appliquer ce fichier en entrée du script, car on sait que l'on aura pas de résultats.

\
Nous conclurons sur ces résultats une fois que nous aurons également les résultats avec des tests plus globaux et représentatifs.

## 3ème partie: chercher à réaliser des tests sur des plages plus globales et représentifs (suite aux soucis évoqués à la fin de la partie 1)

#### *1ère possibilité* : tester toutes les @IP en fesant un saut de x @IP entre chaque IP testé

Tester 100 000 @IP en limitant le débit à 5 requêtes/seconde devrait prendre environ 5h30. Je décide donc de tester environ 100 000 @IP réparties sur la totalité du range des adresses IPv4. 

La totalité des @IP = 4,3 x 10⁹

4,3 x 10⁹/40 000 = 107 000 donc on va tester une @IP toutes les 40 000.

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
On reprend alors le script python (script_ip) que l'on a fait initialement qui générait les adresses IP dans un fichier, on le modifie pour qu'il fasse des sauts de 40 000 IP à chaque itération puis on donnera ce fichier à zmap.

```
import ipaddress
import os


max_ip = 107374 # (2^32 / 40000, car on fait une IP toutes les 40 000)
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
Cette possibilité testant 107 000 @IP prend environ 5h20 à s'executeur. Une fois fait, le fichier de résultats contients seulement **75 @IP avec le port 853 ouvert**. On envoie ensuite des requêtes DoT à ces résultats de la même manière que précédement et **aucune IP ne répond (0%)**.

#### *2ème possibilité* : tester toutes les IP du monde sans limiter le débit :

Avec cette possibilité qui envoie des centaines de milliers de requêtes /seconde, d'une part la box internet est très sollicité et donc beaucoup de paquets seront perdues, et j'effectue ce test en connaissance de cause. Mais il apparait pour moi comme un bon moyen de tester des @IP de manière vraiment aléatoire en couvrant toute l'amplitude des adresses IPv4.

J'utilise donc simplement la commande qui suit et attends qu'elle ait fini de s’exécuter; cela prend un peu moins de 3h.

```sudo zmap -p 853  -o test_all1.csv 0.0.0.0/0```

\
**Nous obtenons 1454 résultats**, donc 1454 @IP avec le port 853 ouvert. Nous appliquons ensuite les requêtes DoT à ces résultats, toujours de la même façon que précédement et nous avons **5 réponses, soit 0,0034%**.

\
**Conclusion sur les réponses aux requêtes DoT des @IP avec le port 853 ouvert:**  

Parmi les tests faits, surtout les derniers qui sont un peu plus représentatifs, nous observons très peu de résultats, que ce soit pour le nombre d'@IP avec le port 853 ouvert et encore plus le nombre d'@IP qui répondent aux requêtes DoT. C'était plutôt attendu, et ces résultats sont cohérents avec ce qui a été présenté dans l'article de référence. (On rappelle que d'après l'article moins de 1% des requêtes DNS du monde sont chiffrées).

Cependant, nous avons bien des résultats "positifs", dans le sens où nous avons trouvé des hôtes qui répondent aux requêtes DoT, ce qui prouve bien que ces serveurs DoT sont présents et existent vraiment.

En outre, nous pouvons remarquer qu'il y a quand même beaucoup d’hôtes (ou d'@IP) qui ne répondent pas aux requêtes DoT alors qu'elles ont le port 853 ouvert. Ce résultat est d'ailleurs mentionné dans l'article; page 5, nous trouvons l'extrait suivant: *"From each Internet-
wide scan, we discover 2 to 3 million hosts with port 853 open (e.g.,
356M on Feb 1 and 230M on May 1), yet a vast majority of them
do not provide DoT (i.e., they cause getdns errors). As shown in
Figure 3, over 1.5K open DoT resolvers are discovered in each scan,
significantly more than the public resolver lists."* 

Or 1,5 k de résolveurs DoT ouverts sur 2 à 3 M de hosts (mettons 2,5 M) revient à une proportion de 0,06%. Avec le dernier scan fait sur toutes les IP du monde sans limites de débit, nous trouvions plus haut une proportion de 0,0034% d'IP répondant aux requêtes DoT en ayant le port 853 ouvert. l'ordre de grandeur n'est pas le même, dû au caractère peu précis du scan (seules 1454 @IP ont été soumis à des requêtes DoT). Mais dans tous les cas, ces valeurs restent très petites, et nos résultats trouvés ne sont pas aberrants, bien que manquant de précision.

\
Nous pouvons alors nous demander pourquoi tant de port 853 sont ouverts sans répondre aux requêtes DoT, et quels peuvent être les autres utilisations de ce port?

Tout d'abord, le port 853 est contenu dans le range des ports normés, c'est à dire des ports spécifiques réservés à une utilité, en l’occurrence à écouter le trafic Dot pour le port 853. Les raisons qui pourraient alors expliquer pourquoi les hôtes ont le port 853 ouvert mais ne répondent pas aux requêtes DoT peuvent être parce que le serveur à qui on effectue la requête filtre mes requêtes, par exemple parce que l'IP de ma machine n'appartient pas à une plage d'IP autorisée par le serveur. Cela peut aussi être une erreur du côté du serveur, soit parce qu'il reçoit trop de trafic, soit à cause d'un problème de configuration. Enfin, il est également possible que le port 853 du serveur soit ouvert pour une autre utilisation, à ce moment spécifique à ce serveur, et configuré manuellement comme tel, auquel cas il ne peut pas répondre aux requêtes DoT.

