import numpy as np


def generate_sin(duration, frequency, sr=22050):
    t = np.linspace(0, duration, int(duration * sr))
    return np.sin(2 * np.pi * frequency * t)


def modulated_signal(modulator, carrier_frequency, sr=22050):
    duration = len(modulator) / sr
    t = np.linspace(0, duration, len(modulator))
    return np.sin(2 * np.pi * carrier_frequency * t + modulator)
