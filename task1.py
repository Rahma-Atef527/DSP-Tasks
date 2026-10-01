import matplotlib.pyplot as plt


def read_signal(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    signal_type = int(lines[0].strip())
    is_periodic = int(lines[1].strip())
    n1 = int(lines[2].strip())

    indices = []
    samples = []

    frequencies = []
    phases = []

    # Time Domain
    if signal_type == 0:

        for line in lines[3:3 + n1]:
            parts = line.split()

            index = int(parts[0])
            amplitude = float(parts[1])

            indices.append(index)
            samples.append(amplitude)

    # Frequency Domain
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


# =========================================================
# ADDITION
# =========================================================

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


# =========================================================
# MULTIPLICATION
# =========================================================

def mul_signal(signal, con):
    result = []

    for value in signal:
        result.append(value * con)

    return result


# =========================================================
# SINGLE SIGNAL - CONTINUOUS
# =========================================================

def plot_continuous(indices, samples, title="Continuous Signal"):

    plt.figure(figsize=(8, 5))

    plt.plot(indices, samples)

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.show()


# =========================================================
# SINGLE SIGNAL - DISCRETE
# =========================================================

def plot_discrete(indices, samples, title="Discrete Signal"):

    plt.figure(figsize=(8, 5))

    plt.stem(indices, samples)

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)

    plt.grid(True)
    plt.tight_layout()

    plt.show()


# =========================================================
# TWO SIGNALS - CONTINUOUS
# =========================================================

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


# =========================================================
# TWO SIGNALS - DISCRETE
# =========================================================

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