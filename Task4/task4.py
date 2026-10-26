from Task4.CompareSignals import SignalsAreEqual
from Task4.Shift_Fold_Signal import Shift_Fold_Signal
from Task4.DerivativeSignal import DerivativeSignal

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

    for i in range(len(samples) - window_size + 1):
        total = 0

        for j in range(window_size):
            total += samples[i + j]

        average = total / window_size

        result_indices.append(i)
        result_samples.append(average)

    return result_indices, result_samples
# ==========================================
# 2. Sharpening - First Derivative
# ==========================================

def first_derivative(indices, samples):
    result_indices = []
    result_samples = []

    for i in range(1, len(samples)):
        result = samples[i] - samples[i - 1]

        result_indices.append(indices[i])
        result_samples.append(result)

    return result_indices, result_samples


# ==========================================
# 3. Sharpening - Second Derivative
# ==========================================

def second_derivative(indices, samples):
    result_indices = []
    result_samples = []

    for i in range(1, len(samples) - 1):
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

    for i in range(len(samples)):
        result_indices.append(indices[i] + k)
        result_samples.append(samples[i])

    return result_indices, result_samples


# ==========================================
# 5. Advance
# ==========================================

def advance_signal(indices, samples, k):
    result_indices = []
    result_samples = []

    for i in range(len(samples)):
        result_indices.append(indices[i] - k)
        result_samples.append(samples[i])

    return result_indices, result_samples

# ==========================================
# 6. Folding
# ==========================================

def fold_signal(indices, samples):
    result_indices = []
    result_samples = []

    for i in range(len(indices) - 1, -1, -1):
        result_indices.append(-indices[i])
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

    dc_component = total / len(samples)

    result_indices = []
    result_samples = []

    for i in range(len(samples)):
        result_indices.append(indices[i])
        result_samples.append(samples[i] - dc_component)

    return result_indices, result_samples
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




