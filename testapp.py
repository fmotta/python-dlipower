
from __future__ import print_function
import dlipower
import sys
import getopt
import time

#server = 'webswitch'
def main(argv):
    server = "192.168.8.222"
    command = "NONE"
    passWd = "1234"
    switchNum = "0"
    user = "admin"
    cycleDelay = 10

    try:
	opts, args = getopt.getopt(argv,"hs:n:c:p:u:",["hostname=","number=","command=","password=","user"])

    except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print('test.py -i <inputfile> -o <outputfile>')
          sys.exit()

       elif opt in ("-s", "--server"):
          server = arg

       elif opt in ("-n", "--number"):
          switchNum = arg

       elif opt in ("-c", "--command"):
          command = arg

       elif opt in ("-p", "--password"):
          passWd = arg

       elif opt in ("-u", "--user"):
          user = arg

    print('Switch Host is: ', server)
    print('SwitchNo is: ', switchNum)
    print('Command is: ', command)
    print('Connecting to a DLI PowerSwitch at ' + server)
    switch = dlipower.PowerSwitch(hostname=server, userid=user, password=passWd)
    if (command == "toggle"):
	result = switch.status(switchNum)
	if (result == 'ON'):
	    print("Toggling Switch: " + switchNum + " from: " + result + " to: OFF")
	    switch.off(switchNum)

	if (result == 'OFF'):
	    print("Toggling Switch: " + switchNum + " from: " + result + " to: ON")
	    switch.on(switchNum)

    if (command == "status"):
	result = switch.status(switchNum)
	print("Switch: " + switchNum + " is [" + result + "]")

    if (command == "cycle"):
	result = switch.status(switchNum)
	print("Switch: " + switchNum + " is [" + result + "]")
	if (result == 'ON'):
	    print(" turning it off...")
	    switch.off(switchNum)
	    time.sleep(cycleDelay)
	    print(" turning it on...")
	    switch.on(switchNum)

	if (result == 'OFF'):
	    print(" turning it on...")
	    switch.on(switchNum)
	    time.sleep(cycleDelay)
	    print(" turning it off...")
	    switch.off(switchNum)

    if (command == "on"):
	switch.on(switchNum)

    if (command == "off"):
	switch.off(switchNum)


    print('The current status of the powerswitch is:')
    print(switch)


if __name__ == "__main__":
   main(sys.argv[1:])

