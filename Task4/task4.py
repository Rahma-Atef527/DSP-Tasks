import os

import numpy as np

from Task4.CompareSignals import SignalsAreEqual
from Task4.Shift_Fold_Signal import Shift_Fold_Signal
from Task4.DerivativeSignal import DerivativeSignal
from Task4.ConvTest import ConvTest

# ==========================================
# Task 4 - Time Domain Operations
# ==========================================


# Read Signal
def read_signal(filename):
    indices = []
    samples = []

    with open(filename, "r") as file:
        file.readline()  # Signal type
        file.readline()  # Is periodic
        number_of_samples = int(file.readline())

        for i in range(number_of_samples):
            line = file.readline().strip()

            if line:
                values = line.split()
                indices.append(int(values[0]))
                samples.append(float(values[1]))

    return indices, samples


# ==========================================
# 1. Moving Average (Smoothing)
# ==========================================

def moving_average(indices, samples, window_size):
    if window_size <= 0:
        raise ValueError("Window size must be greater than zero.")

    if window_size > len(samples):
        raise ValueError("Window size cannot exceed the signal length.")

    result_indices = []
    result_samples = []

    for i in range(len(samples) - window_size + 1): # بحدد بداية window
        total = 0

        for j in range(window_size): #يجمع samples اللى موجودة فى window
            total += samples[i + j]

        average = total / window_size  # calculate mean

        result_indices.append(i)
        result_samples.append(average)

    return result_indices, result_samples
# ==========================================
# 2. Sharpening - First Derivative
# ==========================================

def first_derivative(indices, samples):
    result_indices = []
    result_samples = []

    for i in range(1, len(samples)): # بدانا من 1 لان 0 مفيش حاجة قبلها احسب منها و عشان لو حسبنا من 0 هيطلع -1 و اللي هو اول عنصر
        result = samples[i] - samples[i - 1]  #y(n)=x(n)−x(n−1)

        result_indices.append(indices[i])
        result_samples.append(result)

    return result_indices, result_samples


# ==========================================
# 3. Sharpening - Second Derivative
# ==========================================

def second_derivative(indices, samples):
    result_indices = []
    result_samples = []

    for i in range(1, len(samples) - 1):   #y(n)=x(n+1)−2x(n)+x(n−1)
        result = samples[i + 1] - 2 * samples[i] + samples[i - 1]

        result_indices.append(indices[i])
        result_samples.append(result)

    return result_indices, result_samples
# ==========================================
# 4. Delay
# ==========================================

def delay_signal(indices, samples, k):
    result_indices = []
    result_samples = []

    for i in range(len(samples)): #y(n)=x(n−k)
        result_indices.append(indices[i] + k)  #بنزود الـ Index بمقدار k بيتحرك لقدام يمين
        result_samples.append(samples[i])

    return result_indices, result_samples


# ==========================================
# 5. Advance
# ==========================================

def advance_signal(indices, samples, k):
    result_indices = []
    result_samples = []

    for i in range(len(samples)):  #y(n)=x(n+k)
        result_indices.append(indices[i] - k)  #لأننا بنقدم الإشارة، فكل Index بيتحرك للخلف
        result_samples.append(samples[i])

    return result_indices, result_samples

# ==========================================
# 6. Folding
# ==========================================

def fold_signal(indices, samples):
    result_indices = []
    result_samples = []

    for i in range(len(indices) - 1, -1, -1): #y(n)=x(−n)
        result_indices.append(-indices[i])  # بنعكس حول الصفر اللى موجود يمين هيروح شمال و هكذا
        result_samples.append(samples[i])

    return result_indices, result_samples

# ==========================================
# 7. Remove DC Component in Time Domain
# ==========================================

def remove_dc_component(indices, samples):
    if len(samples) == 0:
        return indices, []

    total = 0

    for i in range(len(samples)):
        total += samples[i]

    dc_component = total / len(samples) #بنحسب mean

    result_indices = []
    result_samples = []

    for i in range(len(samples)): #y(n)=x(n)−Mean
        result_indices.append(indices[i])
        result_samples.append(samples[i] - dc_component) # بنطرح كل سيجنل من المين
    return result_indices, result_samples

# ==========================================
# 8. Convolution
# ==========================================

def convolve(signal1,signal2,idx1=None,idx2=None):
    signal1 = [float(v) for v in signal1]
    signal2 = [float(v) for v in signal2]
    start1 = 0 if idx1 is None else int(idx1[0])
    start2 = 0 if idx2 is None else int(idx2[0])
    N = len(signal1) + len(signal2) - 1
    y = [0.0] * N
    for i in range(len(signal1)):
        for j in range(len(signal2)):
            y[i + j] += signal1[i] * signal2[j]
    indices = list(range(start1 + start2, start1 + start2 + N))
    return indices, y


def read_conv_inputs():
    # Input_conv_Sig1 / Input_conv_Sig2 live in the same folder as this file
    # (with or without a .txt extension).
    folder = os.path.dirname(os.path.abspath(__file__))
    signals = []

    for name in ("Input_conv_Sig1", "Input_conv_Sig2"):
        path = None

        for candidate in (name, name + ".txt"):
            full_path = os.path.join(folder, candidate)

            if os.path.isfile(full_path):
                path = full_path
                break

        if path is None:
            raise FileNotFoundError(
                "Could not find " + name + " in " + folder
            )

        signals.append(read_signal(path))

    (indices1, samples1), (indices2, samples2) = signals

    return indices1, samples1, indices2, samples2

# =========================================================
# TEST CASES
# =========================================================

if __name__ == "__main__":

    # ==========================================
    # Moving Average Test Cases
    # ==========================================
    print("\n========== Moving Average Tests ==========")

    # Test 1
    indices1, samples1 = read_signal("Signal1.txt")

    result_indices1, result_samples1 = moving_average(
        indices1, samples1, 3
    )

    SignalsAreEqual(
        "Moving Average Test 1",
        "OutMovAvgTest1",
        result_indices1,
        result_samples1
    )

    # Test 2
    indices2, samples2 = read_signal("Signal2.txt")

    result_indices2, result_samples2 = moving_average(
        indices2, samples2, 5
    )

    SignalsAreEqual(
        "Moving Average Test 2",
        "OutMovAvgTest2",
        result_indices2,
        result_samples2
    )

    # ==========================================
    # Folding and Shift Tests
    # ==========================================
    print("\n========== Folding and Shift Tests ==========")

    # ==========================================
    # Test 1: Folding
    # ==========================================

    indices, samples = read_signal("input_fold")

    folded_indices, folded_samples = fold_signal(indices, samples)

    Shift_Fold_Signal(
        "Output_fold",
        folded_indices,
        folded_samples
    )

    # ==========================================
    # Test 2: Delay Folded Signal by 500
    # ==========================================

    shifted_indices, shifted_samples = delay_signal(
        folded_indices,
        folded_samples,
        500
    )

    Shift_Fold_Signal(
        "Output_ShifFoldedby500",
        shifted_indices,
        shifted_samples
    )

    # ==========================================
    # Test 3: Advance Folded Signal by 500
    # ==========================================

    advanced_indices, advanced_samples = advance_signal(
        folded_indices,
        folded_samples,
        500
    )

    Shift_Fold_Signal(
        "Output_ShiftFoldedby-500",
        advanced_indices,
        advanced_samples
    )

    # ==========================================
    # Test Derivative
    # ==========================================
    print("\n========== Derivative Tests ==========")

    DerivativeSignal(first_derivative, second_derivative)

    # ==========================================
    # Remove DC Component Test
    # ==========================================
    print("\n========== Remove DC Component Tests ==========")

    indices, samples = read_signal("DC_component_input")

    result_indices, result_samples = remove_dc_component(
        indices,
        samples
    )

    SignalsAreEqual(
        "Remove DC Component Test: ",
        "DC_component_output",
        result_indices,
        result_samples
    )

    # ==========================================
    # Convolution Test
    # ==========================================
    print("\n========== Convolution Tests ==========")

    conv_indices1, conv_samples1, conv_indices2, conv_samples2 = read_conv_inputs()

    conv_result_indices, conv_result_samples = convolve(
        conv_samples1,
        conv_samples2,
        conv_indices1,
        conv_indices2
    )

    ConvTest(
        conv_result_indices,
        conv_result_samples
    )