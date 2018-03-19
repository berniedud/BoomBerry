from pprint import pprint
from time import sleep
from octolib import mc


SLEEPTIME = 0.2

def display_grids():
    while True:
        for colour in ['red','green','blue']:
            pprint(colour)
            pprint(mc.get(colour))

        sleep(SLEEPTIME)

if __name__ == '__main__':
    display_grids()
