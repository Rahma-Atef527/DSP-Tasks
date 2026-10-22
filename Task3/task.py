import numpy as np
import matplotlib.pyplot as plt
from PIL.ImageOps import mirror


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

def modifiy_components(X, mod):
    X = np.array(X, dtype=complex)
    N = len(X)
    for k, (amp,ph) in mod.items():
        k = int(k) % N
        amp = np.abs(X[k]) if amp is None else amp
        ph = np.angle(X[k]) if ph is None else ph
        X[k] = amp * np.exp(1j * ph)
        mirror = (N - k) % N
        if mirror != k:
            X[mirror] = amp * np.exp(-1j * ph)
    return X


# ================= Linking / run section (added) =================
import os
from CompareSignals import SignalsAreEqual
from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift

DC_INPUT = "DC_component_input"
DC_OUTPUT = "DC_component_output"
DFT_INPUT = "input_Signal_DFT"
DFT_OUTPUT = "Output_Signal_DFT_A,Phase"
IDFT_INPUT = "Input_Signal_IDFT_A,Phase"
IDFT_OUTPUT = "Output_Signal_IDFT"


def find_file(name):
    base = os.path.dirname(os.path.abspath(__file__))
    for folder in (base, os.getcwd()):
        for candidate in (name, name + ".txt"):
            path = os.path.join(folder, candidate)
            if os.path.isfile(path):
                return path
    raise FileNotFoundError("Could not find the file: " + name)


def read_pairs(path):
    """Skip the 3 header lines, then read 'a b' pairs (index/sample or amplitude/phase)."""
    with open(path, "r") as f:
        lines = f.read().splitlines()
    a, b = [], []
    for line in lines[3:]:
        parts = line.replace(",", " ").split()
        if len(parts) != 2:
            break
        a.append(float(parts[0].rstrip("fF")))
        b.append(float(parts[1].rstrip("fF")))
    return a, b


def report(task_name, passed):
    print(task_name + (" Test case passed successfully" if passed else " Test case failed"))


def run_tests():
    # ---------- DFT (amplitude and phase do not depend on fs, so fs=1 is used) ----------
    idx, samples = read_pairs(find_file(DFT_INPUT))
    X, freq, amp_norm, phase = fourier_transform(samples, 1)
    amp = np.abs(X)
    exp_amp, exp_phase = read_pairs(find_file(DFT_OUTPUT))
    report("DFT amplitude", SignalComapreAmplitude([round(float(v), 3) for v in amp],
                                                   [round(v, 3) for v in exp_amp]))
    report("DFT phase", SignalComaprePhaseShift([float(v) for v in phase], exp_phase))

    # ---------- IDFT ----------
    idft_amp, idft_phase = read_pairs(find_file(IDFT_INPUT))
    x_idft = reconstruct_signal(np.array(idft_amp) * np.exp(1j * np.array(idft_phase)))
    SignalsAreEqual("IDFT", find_file(IDFT_OUTPUT), list(range(len(x_idft))), list(x_idft))

    # ---------- Remove DC component ----------
    dc_idx, dc_samples = read_pairs(find_file(DC_INPUT))
    y_dc = reconstruct_signal(remove_component(fourier(dc_samples)))
    SignalsAreEqual("DC component", find_file(DC_OUTPUT), [int(i) for i in dc_idx], list(y_dc))


if __name__ == "__main__":
    run_tests()