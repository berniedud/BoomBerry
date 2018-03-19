from octolib import mc, ramp_colour, reset_zeroes, make_wave

reset_zeroes(mc)

make_wave(mc, 'red', centre=(3,3), duration=4, steps=20, magnitude=100)
