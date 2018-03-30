from pprint import pprint
from time import sleep
from octolib import mc


SLEEPTIME = 0.2

def display_grids_print():
    while True:
        for colour in ['red','green','blue']:
            pprint(colour)
            pprint(mc.get(colour))

        sleep(SLEEPTIME)

def display_on_hat():
    red = mc.get('red')
    green = mc.get('green')
    blue = mc.get('blue')
    pixels = []
    for y in range(red.shape[1]):
        row = []
        for x in range(red.shape[0]):
            pixel = (red[x][y], green[x][y], blue[x][y])
            row.append(pixel)
        pixels.append(row)
    print(pixels)
    un.set_pixels(pixels)
    

if __name__ == '__main__':
    try:
        import unicornhat as un
        display_on_hat()
    except:
        display_grids_print()
