
from __future__ import print_function
import dlipower
import sys
import getopt
import time
#from array import array


#server = 'webswitch'
def main(argv):
    server = "192.168.8.222"
    command = "NONE"
    passWd = "1234"
    switchNum = "0"
    switchArray = list()
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
	  switchArray.append(arg)

       elif opt in ("-c", "--command"):
          command = arg

       elif opt in ("-p", "--password"):
          passWd = arg

       elif opt in ("-u", "--user"):
          user = arg

    print('Switch Host is: ', server)
    #print('SwitchNo is: ', switchNum)
    for s in switchArray:
	print('SwitchNo is: ' + s)

    print('Command is: ', command)
    print('Connecting to a DLI PowerSwitch at ' + server)
    #sys.exit()

    switch = dlipower.PowerSwitch(hostname=server, userid=user, password=passWd)
    if (command == "toggle"):
	result = switch.status(switchNum)
	if (result == 'ON'):
	    for s in switchArray:
	        print("Toggling Switch: " + s + " from: " + result + " to: OFF")
	        switch.off(s)

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
	for s in switchArray:
	    print("Turning Switch: " + s + " to: ON")
	    switch.on(s)


    if (command == "off"):
	for s in switchArray:
	    print("Turning Switch: " + s + " to: OFF")
	    switch.off(s)

    print('The current status of the powerswitch is:')
    print(switch)


if __name__ == "__main__":
   main(sys.argv[1:])

