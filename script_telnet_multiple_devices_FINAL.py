from __future__ import print_function
import shlex
import subprocess
import sys
import telnetlib
import getpass

device_raw_list = raw_input('\nDevice(s) to be accessed: ')
device_raw_list = device_raw_list.replace(",", " ")
device_split_list = map(str, device_raw_list.split())

# COLLECTING USERNAME AND PASSWORD
user = raw_input('\nWhat is the username? ')
passw = getpass.getpass ('\nWhat is the password? ')

for device_hostname in device_split_list:

   # TESTING CONNECTIVITY
   pinging = shlex.split('ping -n 2 ' + device_hostname)
   try:
      output = subprocess.check_output(pinging)
   except subprocess.CalledProcessError , e:
      print('\nThe IP {0} is *not* reachable'.format(pinging[-1]))
   else:
      print('\nThe IP {0} is reachable'.format(pinging[-1]))

      # LOGGING IN
      try:
         # TELNET
         tn = telnetlib.Telnet(device_hostname)

         # USERNAME
         tn.read_until(b'Username:', 2)
         tn.write(user + '\n')
        
         # PASSWORD - WITHOUT SHOW WHAT YOU ARE TYPING
         tn.read_until(b'Password:', 2)
         tn.write(passw + '\n')

         # VALIDATING THE CORRECT LOGIN
         try:
            logged = tn.read_until('#', 2)
         
         # RUNNING COMMANDS
            if "#" in logged:
               print('\n\n\nCollecting outputs on {0}, please wait.\n\n\n'.format(device_hostname))
               # OLD: print('\nCollecting outputs on ', device_hostname , ',' ' please wait.' , sep = '')
               tn.write('terminal length 0' + '\n')
               tn.write('show interface description' + '\n')
               tn.write('show ip interface brief' + '\n')
               tn.write('exit'+'\n')
               response = (tn.read_all().decode('ascii'))
            else:
               response = ('\nA FAILURE HAPPENED WHILE AUTHENTICATING')

         finally:
            print(response)
      finally:
         print()