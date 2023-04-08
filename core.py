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

class filter:
    def __init__(self, match):
        self.combine = False
        self.matches = []
        self.matches.append(match)
        return
    
    def add_match(self, match):
        self.matches.append(match)
        return
    
    def combine_enable(self):
        self.combine = True
        return
    
    def combine_disable(self):
        self.combine = False
        return
    
    def suppress(self, input):
        for match in self.matches:
            if re.search(match, input):
                return True
        return False

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

def logp(line, patternlist, filterlist):

    for filter in filterlist:
        if filter.suppress(line):
            message = ''
            break
        else:       
            for pattern in patternlist:
                if re.search(pattern.rexp,line): 
                    message = pattern.color(line)
                    break
                else:
                    message = line
    return message

def monitor(filename,patternlist,filterlist):
    fileh = open(filename, 'r')
    discard = fileh.readlines()
    while True:
        new = fileh.readlines()
        if new:
            print("%s" % logp(new[0].rstrip(),patternlist,filterlist))
        else:
            pass
        time.sleep(1)
    return

patterns = []
patterns.append(pattern('CDT', 'white', 'blue', 'bold'))
filters = []
filters.append(filter('DO NOT PRINT'))
monitor(args.filename,patterns,filters)