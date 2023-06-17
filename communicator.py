from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

client_number = int(input("Enter number of usernames: "))

Popen([executable, 'G:\\Program Files (x86)\\pycharm\\labwno1\\server.py'],
      creationflags=CREATE_NEW_CONSOLE)
for i in range(client_number):
      Popen([executable, 'G:\\Program Files (x86)\\pycharm\\labwno1\\client.py'],
            creationflags=CREATE_NEW_CONSOLE)
