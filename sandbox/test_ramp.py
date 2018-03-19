from octolib import mc, ramp_colour, reset_zeroes

reset_zeroes(mc)

# ramp_colour(mc, 'red', steps=20, duration=3, increment=2)
# ramp_colour(mc, 'red', steps=20, duration=3, increment=-1)
ramp_colour(mc, 'red', ranges=[((3,4),None),(None, (3,4))], steps=10, duration=5, increment=10)
ramp_colour(mc, 'red', ranges=[((5,6),(6,7))], steps=10, duration=5, increment=5)

ramp_colour(mc, 'red', ranges=[(1,None), (None,0)], steps=10, duration=5, increment=25)
ramp_colour(mc, 'red', ranges=[(None,0)], steps=20, duration=3, increment=-5)


ramp_colour(mc, 'green', steps=20, duration=3, increment=2)
ramp_colour(mc, 'blue', steps=20, duration=3, increment=2)
