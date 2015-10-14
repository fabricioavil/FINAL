from __future__ import print_function
import shlex
import subprocess
import sys
import telnetlib
import getpass

# COLLECTING HOSTNAME
device_hostname = raw_input ('\nHostname to collect the outputs: ')

# COLLECTING USERNAME AND PASSWORD
user = raw_input('\nWhat is the username? ')
passw = getpass.getpass ('\nWhat is the password? ')

# TESTING CONNECTIVITY
pinging = shlex.split('ping -n 2 ' + device_hostname)
try:
   output = subprocess.check_output(pinging)
except subprocess.CalledProcessError,e:
   print('\nThe IP {0} is not reachable'.format(pinging[-1]))
   # Could do like: print('\nThe IP {0} is not reachable'.format(device_hostname))
   # Could do like: print('\nThe IP ', device_hostname , ' is not reachable')
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
            print('\nCollecting outputs on ', device_hostname , ',' ' please wait.' , sep = '')
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