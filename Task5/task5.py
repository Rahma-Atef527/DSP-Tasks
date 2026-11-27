import numpy as np
from Task5.CompareSignal import  Compare_Signals


def read_signal(filename):
    indices = []
    samples = []

    with open(filename, "r") as file:
        file.readline()  # Signal Type
        file.readline()  # Is Periodic
        N = int(file.readline())

        for i in range(N):
            line = file.readline().split()
            indices.append(int(line[0]))
            samples.append(float(line[1]))

    return indices, samples

def normalized_cross_correlation(x1, x2=None): # بقدر استخدمها فىAuto-Correlation كمان علشان انا حاطة x2= none
    x1 = np.asarray(x1, dtype=float)
    if x2 is None:
        x2 = x1   # Auto-Correlation.علشان نقدلر نستخدمها فى
    else:
        x2 = np.asarray(x2, dtype=float)   # Cross-Correlation علشان نقدلر نستخدمها فى

    if len(x1) != len(x2):
        raise ValueError("Signals must have the same length")

    N = len(x1)

    denom = np.sqrt(np.sum(x1 ** 2) * np.sum(x2 ** 2)) #Denominator=sqrt{sum x_1^2 * sum x_2^2}


    r = np.array([  #بتعمل Circular Shift للـ Array. علشان نحسب Correlation
        np.sum(x1 * np.roll(x2, -j))
        for j in range(N)])

    rho = r / denom if denom > 0 else np.zeros(N)  #يعني نقسم كل قيمة Correlation على الـ Denominator.

    return list(range(N)), rho.tolist()

#الـ Function دي بتعمل Zero Padding بعدين  Circular Correlation على الطول الجديد.
def normalized_cross_correlation_periodic(x1, x2): #دي Function بتتعامل مع إشارتين Periodic مختلفتين في الطول.
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)

    N = len(x1) + len(x2) - 1  #N = N1 + N2 - 1

    x1 = np.pad(x1, (0, N - len(x1)))
    x2 = np.pad(x2, (0, N - len(x2)))

    return normalized_cross_correlation(x1, x2)

def time_delay(x1, x2, Ts): #- Ts: Sampling Period، يعني الزمن بين كل Sample والتانية.
    lags, rho = normalized_cross_correlation_periodic(x1, x2)

#lags: أماكن الـ Correlation أو الـ Shifts.
#rho: قيم الـ Normalized Correlation.

    max_index = int(np.argmax(np.abs(rho)))

    j = lags[max_index]  #j: الـ Lag اللي وصلنا عنده لأكبر Correlation مطلقة.

    delay = j * float(Ts)

    return delay, j


if __name__ == "__main__":
    print("========== Task 5 Testing ==========")

    # Test 1: Same Length Signals

    indices1, signal1 = read_signal("Corr_input signal1")
    indices2, signal2 = read_signal("Corr_input signal2")

    lags, result = normalized_cross_correlation(signal1, signal2)

    Compare_Signals("CorrOutput", lags, result)


    # Test 2: Different Length Periodic Signals

    indices3, signal3 = read_signal("Corrdiffer_input signal1")
    indices4, signal4 = read_signal("Corrdiffer_input signal2")

    lags, result = normalized_cross_correlation_periodic(signal3, signal4)

    Compare_Signals("CorrOutputdiffer", lags, result)


    print("\n========== Testing Finished ==========")