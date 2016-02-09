###############################################################################
# Creative Commons with Attribution licensed - or BSD which ever has precedence
# Author: Frank Motta
# Warranty:
#     This is a script.
#     It may work.
#     if it does not then you get to fix it if you wish.
#     No liability is attributable for this toward anyone other than the user
###############################################################################
from __future__ import print_function
import dlipower
import sys
import getopt
import time

shortOpts = "hs:n:c:p:u:l"
longOpts = ["hostname=","number=","command=","password=","user=","nolink"]

def usage():
    print("commands: ")
    for o in longOpts:
	print("    --" + o)

def main(argv):
    server = "192.168.0.100"
    command = "NONE"
    passWd = "1234"
#    switchNum = "0"
    switchArray = list()
    user = "admin"
    cycleDelay = 10
    linkedToggle = True
    resultArray = list()

    try:
	opts, args = getopt.getopt(argv, shortOpts, longOpts)

    except getopt.GetoptError:
      usage()
      sys.exit(2)

    for opt, arg in opts:
       if opt == '-h':
	  usage()
          sys.exit()

       elif opt in ("-s", "--server"):
          server = arg

       elif opt in ("-n", "--number"):
	  switchArray.append(arg)

       elif opt in ("-c", "--command"):
          command = arg

       elif opt in ("-p", "--password"):
          passWd = arg

       elif opt in ("-u", "--user"):
          user = arg

       elif opt in ("-l", "--nolink"):
          linkedToggle = False

    print('Switch Host is: ', server)

    for s in switchArray:
	print('SwitchNo is: ' + s)

    print('Command is: ', command)
    print('Connecting to a DLI PowerSwitch at ' + server)

    switch = dlipower.PowerSwitch(hostname=server, userid=user, password=passWd)
    if (command.lower() == "toggle"):
	    for s in switchArray:
		result = switch.status(s)
		if (result == 'ON'):
	            print("Toggling Switch: " + s + " from: " + result + " to: OFF")
	            switch.off(s)

                elif (result == 'OFF'):
	            for s in switchArray:
	                print("Toggling Switch: " + s + " from: " + result + " to: ON")
	                switch.on(s)

    elif (command.lower() == "status"):
	for s in switchArray:
	    result = switch.status(s)
	    print("Switch: " + s + " is [" + result + "]")

    elif (command.lower() == "cycle"):
	if (linkedToggle == False):
	    for s in switchArray:
    	        result = switch.status(s)
	        print("Switch: " + s + " is [" + result + "]")
	        if (result == 'ON'):
	            print(" turning it off...")
	            switch.off(s)
		    print("Waiting: " + str(cycleDelay) + " seconds")
	            time.sleep(cycleDelay)
	            print(" turning it on...")
	            switch.on(s)

	        if (result == 'OFF'):
	            print(" turning it on...")
	            switch.on(s)
		    print("Waiting: " + str(cycleDelay) + " seconds")
	            time.sleep(cycleDelay)
	            print(" turning it off...")
	            switch.off(s)
	else:
	    i = 0
	    for s in switchArray:	# get the state of all the requested switches
    	        resultArray.append(switch.status(s))

	    for s in switchArray:	# now toggle each
	        print("Switch: " + s + " is [" + resultArray[i] + "]")
	        if (resultArray[i] == 'ON'):
	            print(" turning it off...")
	            switch.off(s)

	        if (resultArray[i] == 'OFF'):
	            print(" turning it on...")
	            switch.on(s)
                i = i + 1

	    print("Waiting: " + str(cycleDelay) + " seconds")
            time.sleep(cycleDelay)	# wait
	    i = 0
	    for s in switchArray:	# now toggle back
	        if (resultArray[i] == 'ON'):
	            print("  turning " + s + ": back ON") 
	            switch.on(s)
	        if (resultArray[i] == 'OFF'):
	            print("  turning " + s + ": back OFF") 
	            switch.off(s)
                i = i + 1
	

    elif (command.lower() == "on"):
	for s in switchArray:
	    print("Turning Switch: " + s + " to: ON")
	    switch.on(s)


    elif (command.lower() == "off"):
	for s in switchArray:
	    print("Turning Switch: " + s + " to: OFF")
	    switch.off(s)

    print('The current status of the powerswitch is:')
    print(switch)


if __name__ == "__main__":
   main(sys.argv[1:])

