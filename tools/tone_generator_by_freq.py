import math

from tones import SINE_WAVE
from tones.mixer import Mixer


MULTIPLIER = math.pow(2, 1/5)

def generate_tone_by_frequency(frequency, duration, output_dir):
    mixer = Mixer(44100, 0.5)
    mixer.create_track(0, SINE_WAVE)
    mixer.add_tone(0, frequency=frequency, duration=duration)
    mixer.write_wav(f'{output_dir}/tone_{str(int(frequency)).zfill(4)}_Hz.wav')

# Create wav files for frequencies between 100 and 10000 Hz, in steps of 100 Hz
output_dir = 'test/data/tones_by_frequency'
frequency = 100
while frequency < 10000:
    generate_tone_by_frequency(frequency, 1.0, output_dir)
    frequency = frequency * MULTIPLIER
