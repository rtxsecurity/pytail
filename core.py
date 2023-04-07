import argparse
import time
import colored
import re

parser = argparse.ArgumentParser(
                    prog='pytail',
                    description='tail and apply ansi properties based on log patterns',
                    epilog='report bugs to bugs@rtxsecurity.com')
parser.add_argument('filename')          
args = parser.parse_args()

class pattern:
    def __init__(self, match, fg, bg, attr):
        self.fg=fg
        self.bg=bg
        self.rexp=match
        self.attr=attr
        return
    
    def color(self, input):
        fg = colored.fg(self.fg)
        bg = colored.bg(self.bg)
        attr = colored.attr(self.attr)
        reset = colored.attr('reset')
        message = f'{fg}{bg}{attr}{input}{reset}'
        return message

def logp(line, patternlist):
    for pattern in patternlist:
        if re.search(pattern.rexp,line): 
            print(pattern.color(line))
            break
        else:
            print(line)
    return

def monitor(filename,patternlist):
    fileh = open(filename, 'r')
    discard = fileh.readlines()
    while True:
        new = fileh.readlines()
        if new:
            logp(new[0].rstrip(),patternlist)
        else:
            pass
        time.sleep(1)
    return

patterns = []
patterns.append(pattern('CDT', 'white', 'blue', 'bold'))
monitor(args.filename,patterns)