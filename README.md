# micropython_debugger
A poor man's but effective micropython interactive command line debugger.

As an example in python do the following to enable the debugger:
```python
import ble_ledmatrix_demo

import debugger
debugger.start()

ble_ledmatrix_demo.demo()
```

for a actual session, see recorded example below:

```
carl@ubuntult:~$ picocom /dev/ttyACM1
picocom v2.2

port is        : /dev/ttyACM1
flowcontrol    : none
baudrate is    : 9600
parity is      : none
databits are   : 8
stopbits are   : 1
escape is      : C-a
local echo is  : no
noinit is      : no
noreset is     : no
nolock is      : no
send_cmd is    : sz -vv
receive_cmd is : rz -vv -E
imap is        : 
omap is        : 
emap is        : crcrlf,delbs,

Type [C-a] [C-h] to see available commands

Terminal ready

Stopped at:ble_ledmatrix_demo.py,98
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:b
Give file, line number:ble_ledmatrix_demo.py,56
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:n
Running until next breakpoint...
Stopped at:ble_ledmatrix_demo.py,56
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:n
Running until next breakpoint...
Stopped at:ble_ledmatrix_demo.py,56
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:n
Running until next breakpoint...
Stopped at:ble_ledmatrix_demo.py,56
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:b
Give file, line number:ble_ledmatrix_demo.py,137
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:p
file ble_ledmatrix_demo.py has breakpoints [56, 137]
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:n
Running until next breakpoint...
Stopped at:ble_ledmatrix_demo.py,56
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:n
Running until next breakpoint...
Stopped at:ble_ledmatrix_demo.py,137
Enter to step, 'g' to go, 'gt' to go with linenumber trace, 'n' to go to next breakpoint, 'b' to enter breakpoint, 'p' to print breakoints:g
Running, exit debugger.
```
