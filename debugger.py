#debugger
import sys

STATE_STEP=1
STATE_GO_NEXTBREAKPOINT=2
STATE_GO_NOBREAKPOINTS=3
STATE_GO_NOBREAKPOINTSTRACE=4
currState = STATE_STEP
breakpoints = {}


def printFrame(frame):
	print("%s,%s" %(frame.f_code.co_filename, frame.f_lineno))

def printTb(frame):
	if frame.f_back:
		printTb(frame.f_back)
	printFrame(frame)
	
def doCommand():
	global currState
	while True:
		cmd = input("Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:")
		if cmd == 'b':
			linenumber = None
			file = None
			while linenumber is None or file is None:
				try:
					file, linestr = input("Give file, line number:").split(",")
					file = file.strip()
					linenumber = int(linestr)
					if file not in breakpoints:
						breakpoints[file] = [linenumber]
					else:
						if linenumber not in breakpoints[file]:
							breakpoints[file].append(linenumber)
				except:
					linenumber = None
					file = None
					print("Incorrect linenumber, try again")
		elif cmd == "p":
			if breakpoints == {}:
				print("No breakpoints set.")
			else:
				for file in breakpoints:
					print("file %s has breakpoints %s" %(file, breakpoints[file])) 
		elif cmd == "n":
			currState = STATE_GO_NEXTBREAKPOINT
			print("Running until next breakpoint...")
			break
		elif cmd == "":
			currState = STATE_STEP
			break
		elif cmd == "g":
			currState = STATE_GO_NOBREAKPOINTS
			print("Running, exit debugger.")
			break
		elif cmd == "gt":
			currState = STATE_GO_NOBREAKPOINTSTRACE
			print("Running, with line number tracing, exit debugger.")
			break
		else:
			print("Unknown command, please retry.")
				

def debugCb(frame, a, b):
	global currState
	if currState == STATE_STEP:
		print("Stopped at:", end='')
		printFrame(frame)
		doCommand()
	elif currState == STATE_GO_NEXTBREAKPOINT:
		#check if we have hit a breapoint
		if frame.f_code.co_filename in breakpoints:
			if frame.f_lineno in breakpoints[frame.f_code.co_filename]:
				#hit
				print("Stopped at:", end='')
				printFrame(frame)
				doCommand()
	elif currState == STATE_GO_NOBREAKPOINTS:
		#do not check for breakpoints any more
		pass
	elif currState == STATE_GO_NOBREAKPOINTSTRACE:
		printFrame(frame)
	else:
		print("state error")
	return(debugCb)

def start():
	sys.settrace(debugCb)
	