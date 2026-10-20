import numpy as np
import matplotlib.pyplot as plt

def fourier(data, inverse=False):
    data = np.asarray(data, dtype=complex)
    N = len(data)
    n = np.arange(N)
    sign = 1 if inverse else -1
    W = np.exp(sign * 2j * np.pi * np.outer(n, n) / N)
    out = W @ data
    return out / N if inverse else out

def fourier_transform(signal, fs):
    x = np.asarray(signal, dtype=float)
    N = len(x)
    X = fourier(x)
    freq = np.arange(N) * float(fs) / N
    amp = np.abs(X)
    peak = amp.max()
    amp_norm = amp / peak if peak > 0 else amp.copy()
    phase = np.angle(X)
    phase[amp < 1e-9 * (peak if peak > 0 else 1)] = 0
    return X, freq, amp_norm, phase

def get_dominat(freq, amp_norm, threshold = 0.5):
    freq = np.asarray(freq)
    amp_norm = np.asarray(amp_norm)
    half = len(freq) // 2 + 1
    return freq[:half][amp_norm[:half] > threshold]

def remove_component(X):
    X = np.asarray(X, dtype=complex)
    X[0] = 0
    return X

def reconstruct_signal(X):
    return fourier(X, inverse=True).real