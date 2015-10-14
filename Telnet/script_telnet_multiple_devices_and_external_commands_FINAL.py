from __future__ import print_function
import shlex
import subprocess
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
   ping_cmd = shlex.split('ping -n 2 ' + device_hostname)
   try:
      output = subprocess.check_output(ping_cmd)
   except subprocess.CalledProcessError , e:
      print('\nThe IP {0} is *not* reachable'.format(ping_cmd[-1]))
   else:
      print('\nThe IP {0} is reachable'.format(ping_cmd[-1]))

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
               print('\n\n\nCollecting outputs on {0}, please wait.\n\n\n'.format(device_hostname))
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