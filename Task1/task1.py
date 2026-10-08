#task1 code
import matplotlib.pyplot as plt
from Task1.test import (
    AddSignalSamplesAreEqual,
    MultiplySignalByConst
)

def read_signal(filename):
    with open(filename, "r") as file:
        lines = file.readlines()   #read lines and add them in list

    signal_type = int(lines[0].strip())  #type-> 0:Time Domain ,1:Frequency Domain
    is_periodic = int(lines[1].strip())
    n1 = int(lines[2].strip())   #number of samples or frequency

#Empty Lists
    indices = []   # Time Domain
    samples = []   #Amplitude

    frequencies = []
    phases = []

    # TIME DOMAIN
    if signal_type == 0:

        for line in lines[3:3 + n1]:
            parts = line.split()

            index = int(parts[0])
            amplitude = float(parts[1])

            indices.append(index)
            samples.append(amplitude)

    # FREQUENCY DOMAIN
    elif signal_type == 1:

        for line in lines[3:3 + n1]:
            parts = line.split()

            frequency = float(parts[0])
            amplitude = float(parts[1])
            phase = float(parts[2])

            frequencies.append(frequency)
            samples.append(amplitude)
            phases.append(phase)

    return signal_type, is_periodic, indices, samples, frequencies, phases


# ADD SIGNAL
def add_signal(signals):
    if len(signals) == 0:
        return []

    # All signals must have the same number of samples
    length = len(signals[0])

    for signal in signals:
        if len(signal) != length:
            raise ValueError("All signals must have the same number of samples.")

    result = []

    for i in range(length):
        total = 0

        for signal in signals:
            total += signal[i]

        result.append(total)

    return result


# MULTIPLY SIGNAL BY CONSTANT
def mul_signal(signal, con):
    result = []

    for value in signal:
        result.append(value * con)

    return result


# PLOT CONTINUOUS SIGNAL
def plot_continuous(indices, samples, title="Continuous Signal"):

    plt.figure(figsize=(8, 5))

    plt.plot(indices, samples)

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.show()


# PLOT DISCRETE SIGNAL
def plot_discrete(indices, samples, title="Discrete Signal"):

    plt.figure(figsize=(8, 5))

    plt.stem(indices, samples)

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.show()


# PLOT TWO CONTINUOUS SIGNALS
def plot_two_signals(
    indices1,
    samples1,
    indices2,
    samples2,
    title="Two Continuous Signals"
):

    plt.figure(figsize=(8, 5))

    plt.plot(indices1, samples1, label="Signal 1")
    plt.plot(indices2, samples2, label="Signal 2")

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()


# PLOT TWO DISCRETE SIGNALS
def plot_two_discrete_signals(
    indices1,
    samples1,
    indices2,
    samples2,
    title="Two Discrete Signals"
):

    plt.figure(figsize=(8, 5))

    plt.stem(indices1, samples1, label="Signal 1")
    plt.stem(indices2, samples2, label="Signal 2")

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()


def run_tests():

    signal1 = read_signal("Signal1.txt")

    indices1 = signal1[2]
    samples1 = signal1[3]

    signal2 = read_signal("Signal2.txt")

    indices2 = signal2[2]
    samples2 = signal2[3]

    signal3 = read_signal("Signal3.txt")

    indices3 = signal3[2]
    samples3 = signal3[3]
    # ==========================================
    # SIGNAL 1 + SIGNAL 2
    # ==========================================

    print("\n--- Addition Tests ---")

    result_add_12 = add_signal(
        [samples1, samples2]
    )

    AddSignalSamplesAreEqual(
        "Signal1.txt",
        "Signal2.txt",
        indices1,
        result_add_12
    )

    # ==========================================
    # SIGNAL 1 + SIGNAL 3
    # ==========================================

    result_add_13 = add_signal(
        [samples1, samples3]
    )

    AddSignalSamplesAreEqual(
        "Signal1.txt",
        "Signal3.txt",
        indices1,
        result_add_13
    )

    # ==========================================
    # SIGNAL 1 × 5
    # ==========================================

    print("\n--- Multiplication Tests ---")

    result_mul_1 = mul_signal(
        samples1,
        5
    )

    MultiplySignalByConst(
        5,
        indices1,
        result_mul_1
    )

    # ==========================================
    # SIGNAL 2 × 10
    # ==========================================

    result_mul_2 = mul_signal(
        samples2,
        10
    )

    MultiplySignalByConst(
        10,
        indices2,
        result_mul_2
    )



if __name__ == "__main__":
    run_tests()