from pprint import pprint
from time import sleep
from octolib import mc


SLEEPTIME = 0.05

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
            pixel = (safe_int(red[x][y]), safe_int(green[x][y]), safe_int(blue[x][y]))
            row.append(pixel)
        pixels.append(row)
    #print(pixels)
    un.set_pixels(pixels)
    un.show()
    sleep(SLEEPTIME)
    

def safe_int(i):
    try:
        safe_int = max(min(i, 255), 0)
    except:
        safe_int = 0
    return safe_int


if __name__ == '__main__':
        import unicornhat as un
        while True:
        #for _ in range(1000): 
            display_on_hat()
            sleep(SLEEPTIME)
