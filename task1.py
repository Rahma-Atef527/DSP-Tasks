import matplotlib.pyplot as plt

def read_signal(filename):
    with open(filename, "r") as file:

        lines = file.readlines()

    # Read information from the first 3 lines
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

def add_signal(signals):
    result = []

    for i in range(len(signals[0])):
        total = 0

        for signal in signals:
            total+= signal[i]

        result.append(total)
    return result

def mul_signal(signal, con):
    result = []

    for value in signal:
        result.append(value * con)

    return result

def plot_continuous(indices, samples):

    plt.figure()

    plt.plot(indices, samples)

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Continuous Signal")

    plt.grid(True)

    plt.show()

def plot_discrete(indices, samples):

    plt.figure()

    plt.stem(indices, samples)

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Discrete Signal")

    plt.grid(True)

    plt.show()

def plot_two_signals(indices1, samples1, indices2, samples2):
        plt.figure()

        plt.plot(indices1, samples1, label="Signal 1")
        plt.plot(indices2, samples2, label="Signal 2")

        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.title("Two Signals")

        plt.legend()
        plt.grid(True)

        plt.show()

def plot_two_discrete_signals(indices1, samples1, indices2, samples2):

    plt.figure()

    plt.stem(indices1, samples1, label="Signal 1")
    plt.stem(indices2, samples2, label="Signal 2")

    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Two Discrete Signals")

    plt.legend()
    plt.grid(True)

    plt.show()