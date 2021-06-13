#!/usr/bin/env python3

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






