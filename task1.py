import matplotlib.pyplot as plt

def read_signal(filename):

    indices = []
    samples = []

    with open(filename, "r") as file:

        lines = file.readlines()

        for line in lines[3:]:

            parts = line.split()

            if len(parts) >= 2:

                n = int(parts[0])
                value = float(parts[1])

                indices.append(n)
                samples.append(value)

    return indices, samples

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

def plot_cont(n, x):
    plt.plot(n,x)
    plt.xlabel("n")
    plt.ylabel("amp")
    plt.title("continuous plot")
    plt.grid()
    plt.show()

def plot_discrete(n,x):
    plt.stem(n,x)
    plt.xlabel("n")
    plt.ylabel("amp")
    plt.title("discrete plot")
    plt.grid()
    plt.show()