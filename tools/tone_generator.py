"""
Create tones using the tones package, for testing purposes.
Example code can be found here: https://pypi.org/project/tones/
"""
from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer

def generate_tone(note, octave, number, output_dir):
    mixer = Mixer(44100, 0.5)
    mixer.create_track(0, SINE_WAVE)
    mixer.add_note(0, note=note, octave=octave, duration=1.0)
    mixer.write_wav(f'{output_dir}/tone_{octave}{number}{note}.wav')

# Create wav files for each note in the C-major scale, from C4 to C7
output_dir = 'test/data/tones_by_note'
for octave in range(4, 7):
    for number, note in enumerate(['c', 'd', 'e', 'f', 'g', 'a', 'b']):
        generate_tone(note, octave, number, output_dir)
        # Create a file for C7:
generate_tone('c', 7, 0, output_dir)


"""
# Example code:

# Create two monophonic tracks that will play simultaneously, and set
# initial values for note attack, decay and vibrato frequency (these can
# be changed again at any time, see documentation for tones.Mixer
mixer.create_track(0, SAWTOOTH_WAVE, vibrato_frequency=7.0, vibrato_variance=30.0, attack=0.01, decay=0.1)
mixer.create_track(1, SINE_WAVE, attack=0.01, decay=0.1)

# Add a 1-second tone on track 0, slide pitch from c# to f#)
mixer.add_note(0, note='c#', octave=5, duration=1.0, endnote='f#')

# Add a 1-second tone on track 1, slide pitch from f# to g#)
mixer.add_note(1, note='f#', octave=5, duration=1.0, endnote='g#')

# Mix all tracks into a single list of samples and write to .wav file
mixer.write_wav('tones.wav')

# Mix all tracks into a single list of samples scaled from 0.0 to 1.0, and
# return the sample list
samples = mixer.mix()
"""
