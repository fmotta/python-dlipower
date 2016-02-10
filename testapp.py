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

shortOpts = "d:hs:n:c:p:u:lbom:"
longOpts = ["delay=","hostname=","number=","command=","password=","user=","backup","nolink", "config", "name="]
commands = ["rename", "toggle", "status", "cycle", "on", "off", "save"]

def usage():
    print("Options:")
    for o in longOpts:
	print("    --" + o)

    print("Valid commands:")
    for c in commands:
	print("      " + c)

def validCommand(cmd):
    if cmd in commands:
	return True

    print("Invalid command: " + cmd)
    return False


def main(argv):
    server = "192.168.0.100"
    command = "NONE"
    passWd = "1234"
    switchArray = list()
    user = "admin"
    cycleDelay = 10
    linkedToggle = True
    resultArray = list()
    backupConfig = False
    loadConfig = False
    switchNameArray = list()
    VerboseOutput = True

    try:
	opts, args = getopt.getopt(argv, shortOpts, longOpts)

    except getopt.GetoptError:
      usage()
      sys.exit(2)

    # Process args
    for opt, arg in opts:
       if opt == '-h':
	  usage()
          sys.exit()

       # NOTE: Config is stored in clear text
       elif opt in ("-b", "--backup"):
	  print("\n\nWARNING: Configuration is saved in clear text and includes the password!\n\n")
          backupConfig = True

       # FIXME - TODO load configuration
       elif opt in ("-o", "--config"):
          LoadConfig = True

       elif opt in ("-s", "--server"):
          server = arg

       elif opt in ("-n", "--number"):
	  switchArray.append(arg)

       elif opt in ("-m", "--name"):
          switchNameArray.append(arg)

       elif opt in ("-c", "--command"):
          command = arg

       elif opt in ("-p", "--password"):
          passWd = arg

       elif opt in ("-u", "--user"):
          user = arg

       elif opt in ("-d", "--delay"):
          cycleDelay = arg

       elif opt in ("-l", "--nolink"):
          linkedToggle = False

    if (validCommand(command) == False):
	usage()
	sys.exit(1)

    # Report settings (rather verbose for now)
    if (VerboseOutput == True):
        print('Switch Host is: ', server)

        for s in switchArray:
    	   print('SwitchNo is: ' + s)

        print('Command is: ', command)
        print('Cycle Delay is: ', cycleDelay)
        print('Connecting to a DLI PowerSwitch at ' + server)

    # Connect to switch and try to handle an exception
    try:
	switch = dlipower.PowerSwitch(hostname=server, userid=user, password=passWd)

    # Yep - cannot find an exception routine that helps find a failed connection...
    # So... here are some attempts that cannot seem to prevent a Traceback from a failed connect
    # Probably my error/problem
    except dlipower.ValueError:
        print("Exception connecting to switch")
	sys.exit(0xff)

    if (switch.verify() == False):
        print("Exception connecting to switch")
	sys.exit(0xff)


    # Process commands
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

    elif (command.lower() == "rename"):
	# Simple sequentially rename - meh easy to understand - first switch number passed as an argument gets the first name passed.  Then the second and ...
	i = 0
	for s in switchNameArray:
	    sName = switchArray[i]
            tName = switchNameArray[i]
	    print("SNA: " + tName)
	    print("Naming Switch: " + sName + " to: " + s)
            switch[int(sName)-1].name = tName
	    i = i + 1

    elif (command.lower() == "status"):
	for s in switchArray:
	    result = switch.status(s)
	    print("Switch: " + s + " is [" + result + "]")

    elif (command.lower() == "cycle"):
	if (linkedToggle == False):   # Toggle ALL the requested switches (inverse of present state), pause, then toggle them back to last state
	    for s in switchArray:
    	        result = switch.status(s)
	        print("Switch: " + s + " is [" + result + "]")
	        if (result == 'ON'):
	            print(" turning it off...")
	            switch.off(s)
		    print("Waiting: " + str(cycleDelay) + " seconds")
	            time.sleep(float(cycleDelay))
	            print(" turning it on...")
	            switch.on(s)

	        if (result == 'OFF'):
	            print(" turning it on...")
	            switch.on(s)
		    print("Waiting: " + str(cycleDelay) + " seconds")
	            time.sleep(float(cycleDelay))
	            print(" turning it off...")
	            switch.off(s)
	else:	# This is the default path - toggle the requested switches(inverse of present state), wait a bit, toggle them back to last state
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
            time.sleep(float(cycleDelay))	# wait
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
    else:
	usage()
	sys.exit(1)

    print('The current status of the powerswitch is:')
    print(switch)

    if (backupConfig == True):
	switch.save_configuration()


if __name__ == "__main__":
   main(sys.argv[1:])

