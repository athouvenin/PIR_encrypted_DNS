



import ipaddress
import os


max_ip = 107374 # (2^32 / 40000, car on fait une ip toutes les 40 000)
une_ip = ipaddress.ip_address('0.0.0.0')

with open('all_ips_40.txt', 'w') as f:
    for i in range(0, max_ip):
        
        f.write("%s\n" % une_ip)
        une_ip = une_ip + 40000

       

print('finished')



