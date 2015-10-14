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
      # COMMANDS TO RUN
      selected_cmd_file = open("cmd_file.txt", 'r')

      # STARTING FROM THE BEGINNING OF THE FILE
      selected_cmd_file.seek(0)

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
            for each_line in selected_cmd_file.readlines():
               tn.write(each_line + '\n')
            response = (tn.read_all().decode('ascii'))
            tn.close()
         else:
            response = ('\nA FAILURE HAPPENED WHILE AUTHENTICATING')
            tn.close()

      finally:
         print(response)

      # CLOSING THE FILE
      selected_cmd_file.close()
   finally:
      print()