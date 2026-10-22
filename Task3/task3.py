import numpy as np
import matplotlib.pyplot as plt
import math

from Task3.signalcompare import (
    SignalComapreAmplitude,
    SignalComaprePhaseShift
)

from Task3.CompareSignals import (
SignalsAreEqual
)

# =====================================================
# DFT AND IDFT USING ONE FUNCTION
# =====================================================

def fourier(data, inverse=False):

    data = np.asarray(data, dtype=complex)  #complex:z=a+jb
    N = len(data)  #total number of samples

    if N == 0:
        return np.array([], dtype=complex)

    n = np.arange(N)   #index:[0,1,2,...]

    if inverse:  #true
        sign = 1    #j sign (+) IDFT
    else:     #false
        sign = -1    #j sign (-) DFT

    W = np.exp(sign * 2j * np.pi * np.outer(n, n) / N)  #j2πkn/N or (-j2πkn/N)

    result = W @ data

    if inverse:
        result = result / N

    return result


# =====================================================
# FOURIER TRANSFORM
# =====================================================

def fourier_transform(signal, fs):  #fs:Sampling Frequency.

    signal = np.asarray(signal, dtype=float)

    if len(signal) == 0:
        raise ValueError("Signal cannot be empty.")

    if fs <= 0:
        raise ValueError("Sampling frequency must be positive.")

    N = len(signal)

    X = fourier(signal)  #calculate DFT

    frequencies = np.arange(N) * fs / N    #fk=k*fs/N التردد رقم k.

    amplitude = np.abs(X)

    peak = amplitude.max()  #هنستخدم أكبر قيمة دي علشان نعمل Normalization

    if peak > 0:
        normalized_amplitude = amplitude / peak     #بنقسم كل قيمة Amplitude على أكبر قيمة موجودة علشان نخليها بين 0و1
    else:
        normalized_amplitude = amplitude.copy()     #لو اكبر قيمة ب0 ننسخ كل القسم زى ماهى

    phase = np.array([
        math.atan2(value.imag, value.real)
        for value in X
    ])

    if peak > 0:
        phase[amplitude < 1e-9 * peak] = 0

    return X, frequencies, normalized_amplitude, phase


# =====================================================
# GET DOMINANT FREQUENCIES
# =====================================================

def get_dominant(frequencies, normalized_amplitude, threshold=0.5):

    frequencies = np.asarray(frequencies)
    normalized_amplitude = np.asarray(normalized_amplitude)

    half = len(frequencies) // 2 + 1

    dominant = frequencies[:half][      #if frequencies = [0, 1, 2, 3, 4, 5] and  half = 4 then: result =[0, 1, 2, 3]
        normalized_amplitude[:half] > threshold     #normalized_amplitude = [1.0, 0.2, 0.7, 0.4]  ,threshold = 0.5   , result=[True, False, True, False],
    ]  #dominant = [0, 2]

    return dominant


# =====================================================
# MODIFY AMPLITUDE AND PHASE
# =====================================================

def modify_components(X, index, amplitude, phase):

    X = np.asarray(X, dtype=complex).copy()

    N = len(X)

    if index < 0 or index >= N:
        raise ValueError("Invalid frequency component index.")

    if amplitude < 0:
        raise ValueError("Amplitude cannot be negative.")

    # Phase is entered in radians
    X[index] = amplitude * np.exp(1j * phase)   #X[k]=Ae ^jθ

    # Preserve conjugate symmetry for real signals
    if index != 0 and not (
        N % 2 == 0 and index == N // 2
    ):
        X[-index] = np.conjugate(X[index])

    return X


# =====================================================
# REMOVE DC COMPONENT
# =====================================================

def remove_component(X):        #الـ DC Component هو معامل الـ DFT الموجود عند التردد صفر، F(0)

    X = np.asarray(X, dtype=complex).copy()

    if len(X) > 0:
        X[0] = 0

    return X


# =====================================================
# RECONSTRUCT SIGNAL USING IDFT
# =====================================================

def reconstruct_signal(X):

    reconstructed = fourier(X, inverse=True)

    return reconstructed.real


# =====================================================
# READ TIME-DOMAIN SIGNAL
# =====================================================

def read_signal(filename):

    with open(filename, "r") as file:

        lines = file.readlines()

    signal_type = int(lines[0].strip())
    periodic = int(lines[1].strip())
    N = int(lines[2].strip())

    indices = []
    samples = []

    for i in range(N):

        values = lines[i + 3].split()

        indices.append(float(values[0]))
        samples.append(float(values[1]))

    return signal_type, periodic, indices, samples


# =====================================================
# READ DFT OUTPUT FILE
# =====================================================

def read_dft_output(filename):

    expected_amplitude = []
    expected_phase = []

    with open(filename, "r") as file:

        file.readline()
        file.readline()

        N = int(file.readline().strip())

        for i in range(N):

            line = file.readline().strip()

            values = line.split()

            amplitude = float(values[0].rstrip("fF"))
            phase = float(values[1].rstrip("fF"))

            expected_amplitude.append(amplitude)
            expected_phase.append(phase)

    return expected_amplitude, expected_phase


# =====================================================
# READ IDFT AMPLITUDE AND PHASE
# =====================================================

def read_amplitude_phase(filename):

    amplitude = []
    phase = []

    with open(filename, "r") as file:

        lines = file.readlines()

    N = int(lines[2].strip())

    for i in range(N):

        values = lines[i + 3].split()

        amplitude.append(float(values[0].rstrip("fF")))
        phase.append(float(values[1].rstrip("fF")))

    return amplitude, phase


# =====================================================
# READ EXPECTED IDFT OUTPUT
# =====================================================

def read_idft_output(filename):

    expected_signal = []

    with open(filename, "r") as file:

        lines = file.readlines()

    N = int(lines[2].strip())

    for i in range(N):

        values = lines[i + 3].split()

        expected_signal.append(float(values[1]))

    return expected_signal
#==============================
    # TEST CASES
#==============================

if __name__ == "__main__":

    print("=" * 60)
    print("                 TASK 3 TEST CASES")
    print("=" * 60)

#==============================
    # DFT TEST
#==============================

    print("\n--- DFT Test ---")

    signal = read_signal("input_Signal_DFT")
    samples = signal[3]

    dft_result = fourier(samples)

    # Read expected results
    expected_amplitudes, expected_phases = read_dft_output(
        "Output_Signal_DFT_A,Phase"
    )

    # Calculate actual results
    calculated_amplitudes = np.abs(dft_result).tolist()
    calculated_phases = np.angle(dft_result).tolist()

    # Compare amplitude
    amplitude_result = SignalComapreAmplitude(
        expected_amplitudes,
        calculated_amplitudes
    )

    # Compare phase
    phase_result = SignalComaprePhaseShift(
        expected_phases,
        calculated_phases
    )

    print("DFT Amplitude Test:", amplitude_result," ,Test case passed successfully")
    print("DFT Phase Test:", phase_result," ,Test case passed successfully")

#=================================
    # IDFT TEST
#=================================

    print("\n--- IDFT Test ---")

    amplitudes, phases = read_amplitude_phase(
        "Input_Signal_IDFT_A,Phase"
    )

    frequency_components = []

    for i in range(len(amplitudes)):
        component = amplitudes[i] * np.exp(1j * phases[i])
        frequency_components.append(component)

    reconstructed = reconstruct_signal(frequency_components)

    expected_samples = read_idft_output("Output_Signal_IDFT")

    idft_result = SignalComapreAmplitude(
        expected_samples,
        reconstructed.tolist()
    )

    print("IDFT Test:", idft_result," ,Test case passed successfully")

#=======================
    # DC COMPONENT TEST
#=======================

    print("\n--- DC Component Test ---")

    # Read input signal
    dc_signal = read_signal("DC_component_input")
    dc_samples = dc_signal[3]

    # Calculate DFT
    dc_dft = fourier(dc_samples)

    # Remove DC component
    dc_dft = remove_component(dc_dft)

    # Reconstruct signal using IDFT
    dc_output = reconstruct_signal(dc_dft)

    # Read indices from input signal
    dc_indices = dc_signal[2]

    # Compare with expected output
    SignalsAreEqual(
        "DC Component Removal",
        "DC_component_output",
        dc_indices,
        dc_output.tolist()
    )

# =====================================================
# PLOT FREQUENCY DOMAIN
# =====================================================

def plot_frequency_domain(frequencies, amplitude, phase):

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)

    plt.stem(frequencies, amplitude)

    plt.title("Frequency vs Amplitude")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Amplitude")

    plt.grid(True)

    plt.subplot(1, 2, 2)

    plt.stem(frequencies, phase)

    plt.title("Frequency vs Phase")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (Radians)")

    plt.grid(True)
    plt.tight_layout()

    plt.show()
