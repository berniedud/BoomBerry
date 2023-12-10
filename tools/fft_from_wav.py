"""
Create fft array from wav file
"""

import argparse
from scipy import signal, fftpack
from scipy.io import wavfile


def main():
    parser = argparse.ArgumentParser(description='Create fft array from wav file')
    parser.add_argument('input_file', type=str, help='input file')
    parser.add_argument('--window_size', type=int, default=1024, help='window size')
    parser.add_argument('--window_step', type=int, default=512, help='window step')
    parser.add_argument('--fft_size', type=int, default=1024, help='fft size')
    args = parser.parse_args()

    print(args)

    # Read wav file
    window_size = args.window_size
    window_step = args.window_step
    fft_size = args.fft_size

    sample_rate, samples = wavfile.read(args.input_file)
    print(f'sample_rate: {sample_rate}')
    print(f'samples shape: {samples.shape}')
    sample_count = len(samples)
    print(f'samples count: {sample_count}')

    plot_waveform(samples[:len(samples)//100])

    exit(0)
    # Create fft array
    f, t, Zxx = signal.stft(samples, fs=sample_rate, window='hann', nperseg=window_size, noverlap=window_size-window_step, nfft=fft_size)
    print(f'f: {f}')
    print(f't: {t}')
    print(f'Zxx: {Zxx}')
    print(f'Zxx.shape: {Zxx.shape}')
    print(f'Zxx.shape[0]: {Zxx.shape[0]}')


def plot_waveform(samples):
    # expects 1/100th of a second of samples
    import matplotlib.pyplot as plt
    import numpy as np
    time = np.linspace(0., 0.01, int(len(samples)))
    plt.plot(time, samples, label="mono channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


if __name__ == '__main__':
    main()
