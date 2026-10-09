import math
from Task2.QuanTest1 import QuantizationTest1
from Task2.QuanTest2 import QuantizationTest2
from Task2.test import SignalSamplesAreEqual

# Read Signal
def read_signal(filename):

    samples = []

    with open(filename, "r") as file:

        file.readline()
        file.readline()

        n = int(file.readline())

        for _ in range(n):

            line = file.readline().strip()

            if line:
                parts = line.split()

                sample = float(parts[1])
                samples.append(sample)

    return samples

# Arithmetic Operations
def sub_signal(signal1, signal2):
    if len(signal1) != len(signal2):
        raise ValueError("Signals must have the same number of samples")
    res = []
    for i in range(len(signal1)):
        res.append(abs(signal1[i] - signal2[i]))
    return res


def square_signal(signal):
    res = []
    for val in signal:
        res.append(val * val)
    return res


def normalize_signal(signal, choice):
    if len(signal) == 0:
        return []
    min_val = min(signal)
    max_val = max(signal)
    if max_val == min_val:
        raise ValueError("constant signal cannot be normalized")
    
    res = []
    for val in signal:
        scaled = (val - min_val) / (max_val - min_val)

        if choice == 1:
            res.append(2 * scaled - 1)
        elif choice == 2:
            res.append(scaled)
        else:
            raise ValueError("choice must be 1 (-1 to 1) or 2 (0 to 1)")

    return res


def accumulate_signal(signal):
    res = []
    total = 0

    for val in signal:
        total += val
        res.append(total)

    return res


# Quantization
def quantize_signal(samples, bits=None, levels=None):
    # Calculate number of levels
    if bits is not None:
        levels = 2 ** bits
    elif levels is not None:
        bits = math.ceil(math.log2(levels))

    minimum = min(samples)
    maximum = max(samples)

    delta = (maximum - minimum) / levels

    interval_indices = []
    encoded_values = []
    quantized_values = []
    sampled_error = []

    for sample in samples:

        # Find interval
        interval = int((sample - minimum) / delta)

        # Handle maximum value
        if interval >= levels:
            interval = levels - 1

        # Interval index starts from 1
        interval_index = interval + 1

        # Calculate interval boundaries
        lower = minimum + interval * delta
        upper = lower + delta

        # Quantized value = midpoint
        quantized = (lower + upper) / 2

        # Encoding
        encoded = format(interval, f"0{bits}b")

        # Error
        error = quantized - sample

        interval_indices.append(interval_index)
        encoded_values.append(encoded)
        quantized_values.append(quantized)
        sampled_error.append(error)

    return (
        interval_indices,
        encoded_values,
        quantized_values,
        sampled_error
    )

# TEST CASES

if __name__ == "__main__":

    print("=" * 60)
    print("                 TASK 2 TEST CASES")
    print("=" * 60)


    # Read indices from the input file
    def read_indices(filename):
        indices = []

        with open(filename, "r") as file:
            file.readline()
            file.readline()
            n = int(file.readline())

            for _ in range(n):
                line = file.readline().strip()

                if line:
                    indices.append(int(line.split()[0]))

        return indices


    # SUBTRACTION TEST 1: Signal1 - Signal2
    print("\n--- Subtraction Test 1: Signal1 - Signal2 ---")

    signal1 = read_signal("Signal1.txt")
    signal2 = read_signal("Signal2.txt")

    result = sub_signal(signal1, signal2)

    indices = read_indices("Signal1.txt")

    SignalSamplesAreEqual(
        "Subtraction Signal1 - Signal2",
        "signal1-signal2",
        indices,
        result
    )

    # SUBTRACTION TEST 2: Signal1 - Signal3
    print("\n--- Subtraction Test 2: Signal1 - Signal3 ---")

    signal1 = read_signal("Signal1.txt")
    signal3 = read_signal("signal3.txt")

    result = sub_signal(signal1, signal3)

    indices = read_indices("Signal1.txt")

    SignalSamplesAreEqual(
        "Subtraction Signal1 - Signal3",
        "signal1-signal3",
        indices,
        result
    )

    # Squaring Test
    print("\n--- Squaring Test ---")

    signal1 = read_signal("Signal1.txt")

    result = square_signal(signal1)

    indices = read_indices("Signal1.txt")

    SignalSamplesAreEqual(
        "Squaring",
        "Output squaring signal 1",
        indices,
        result
    )

    # Normalization Test 1: -1 to 1
    print("\n--- Normalization Test 1 ---")

    signal1 = read_signal("Signal1.txt")

    result = normalize_signal(
        signal1,
        1
    )

    indices = read_indices("Signal1.txt")

    SignalSamplesAreEqual(
        "Normalization (-1 to 1)",
        "normalize of signal 1 (from -1 to 1)-- output",
        indices,
        result
    )

    # Normalization Test 2: 0 to 1
    print("\n--- Normalization Test 2 ---")

    signal2 = read_signal("Signal2.txt")

    result = normalize_signal(
        signal2,
        2
    )

    indices = read_indices("Signal2.txt")

    SignalSamplesAreEqual(
        "Normalization (0 to 1)",
        "normlize signal 2 (from 0 to 1 )-- output",
        indices,
        result
    )

    # Accumulation Test
    print("\n--- Accumulation Test ---")

    signal1 = read_signal("Signal1.txt")

    result = accumulate_signal(signal1)

    indices = read_indices("Signal1.txt")

    SignalSamplesAreEqual(
        "Accumulation",
        "output accumulation for signal1",
        indices,
        result
    )

    # Quantization Test 1
# Number of Bits = 3

    print("\n--- Quantization Test 1 ---")

    samples1 = read_signal("Quan1_input")

    (
        interval_indices1,
        encoded_values1,
        quantized_values1,
        sampled_error1
    ) = quantize_signal(
        samples1,
        bits=3
    )

    QuantizationTest1(
        "Quan1_Out",
        encoded_values1,
        quantized_values1
    )

 # Quantization Test 2
 # Number of Levels = 4

    print("\n--- Quantization Test 2 ---")

    samples2 = read_signal("Quan2_input")

    (
        interval_indices2,
        encoded_values2,
        quantized_values2,
        sampled_error2
    ) = quantize_signal(
        samples2,
        levels=4
    )

    QuantizationTest2(
        "Quan2_Out",
        interval_indices2,
        encoded_values2,
        quantized_values2,
        sampled_error2
    )
