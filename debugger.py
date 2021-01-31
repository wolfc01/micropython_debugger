#
# Simple micropython debugger, to be used at the same port where also the REPL is executed.
# Built on the settrace function which has been added by https://github.com/dpgeorge, at issue https://github.com/micropython/micropython/pull/5026
#
# mpconfigport.h has to be changed for this:
# define MICROPY_PY_SYS_SETTRACE       (1) // To activate sys.settrace(tracefunc)
# define MICROPY_COMP_CONST            (0) // required for MICROPY_PY_SYS_SETTRACE
# define MICROPY_PERSISTENT_CODE_SAVE  (1) // required for MICROPY_PY_SYS_SETTRACE

import sys
import micropython

STATE_STEP=1
STATE_GO_NEXTBREAKPOINT=2
STATE_GO_NOBREAKPOINTS=3
STATE_GO_NOBREAKPOINTSTRACE=4
currState = STATE_STEP
breakpoints = {}

breakcounter = 0
show_breakcounter = False


def printFrame(frame, showCount=False):
	if showCount == False:
		print('File "%s", line %s, in %s' %(frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name))
	else:
		print('[%6d] File "%s", line %s, in %s' %(breakcounter, frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name))
	#print(dir(frame))
	#print(frame.f_globals)

def printTb(frame):
	if frame.f_back:
		printTb(frame.f_back)
	printFrame(frame)
	
def doCommand(frame):
	global currState
	global breakcounter
	global show_breakcounter
	while True:
		cmd = input("Debugger,? for help >")
		if cmd == '?':
			s = "help:\n<enter>:step\n'g'    :go\n'gt'   :go with linenr trace\n'n'    :goto next break\n'b'    :enter breakpoint\n'p'    :print breakpoints\n'bt'   :backtrace\n'bc'   :toggle breakcounter\n'v'    :print global variables\n'r'    :REPL in current scope\n'm'    :memory info"
			print(s) 
		elif cmd == 'bc':
			show_breakcounter = not(show_breakcounter)
		elif cmd == 'b':
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
		elif cmd == "bt":
			printTb(frame)
		elif cmd == 'v':
			for v in frame.f_globals:
				if str(type(frame.f_globals[v])) not in ["<class 'type'>", "<class 'function'>", "<class 'module'>" ]:
					print("%s:%s %s" %(v, frame.f_globals[v], str(type(frame.f_globals[v]))))
		elif cmd == 'r':
			print("Entering REPL in current scope, CTRL-D to exit this REPL.")
			while True:
				try:
					s = input(">>>")
				except EOFError:
					break #leave this repl.
				try:
					exec(s)
				except Exception as e:
					sys.print_exception(e)
		elif cmd == "m":
			print("memory usage figures:")
			print("---------------------")
			print("micropython.mem_info(1)")
			micropython.mem_info(1)
			print("micropython.stack_use=%s" %micropython.stack_use())
		else:
			print("Unknown command, please retry.")
				

def debugCb(frame, a, b):
	global currState
	global breakcounter
	global show_breakcounter
	breakcounter += 1
	if currState == STATE_STEP:
		print("Stopped at:", end='')
		printFrame(frame)
		doCommand(frame)
	elif currState == STATE_GO_NEXTBREAKPOINT:
		#check if we have hit a breakpoint
		if frame.f_code.co_filename in breakpoints:
			if frame.f_lineno in breakpoints[frame.f_code.co_filename]:
				#hit
				print("Stopped at:", end='')
				printFrame(frame)
				doCommand(frame)
	elif currState == STATE_GO_NOBREAKPOINTS:
		#do not check for breakpoints any more
		pass
	elif currState == STATE_GO_NOBREAKPOINTSTRACE:
		printFrame(frame, show_breakcounter)
	else:
		print("state error")
	return(debugCb)

def start():
	sys.settrace(debugCb)
	
