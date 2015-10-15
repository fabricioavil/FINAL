import subprocess
import os

destinations = ["www.google.com" , "8.8.8.8" , "192.168.1.254"]

result = 0

for each_destination in destinations:

    ping_cmd = os.system("ping -c 3 " + each_destination)
    if ping_cmd == 0:
        print("\n" , each_destination , 'is up!\n')
        result += result + 1
    else:
        print("\n" , each_destination , "is down!\n")

if result == 0:
    subprocess.check_call("/sbin/shutdown -r now" , shell=True)