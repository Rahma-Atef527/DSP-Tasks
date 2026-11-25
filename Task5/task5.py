import numpy as np

def normalized_cross_correlation(x1, x2=None):
    x1 = np.asarray(x1, dtype=float)
    x2 = x1 if x2 is None else np.asarray(x2, dtype=float)
    if len(x1) != len(x2):
        raise ValueError("Signals must have the same length")
    N = len(x1)
    denom = np.sqrt(np.sum(x1 ** 2) * np.sum(x2 ** 2))
    r = np.array([np.sum(x1 * np.roll(x2, -j)) for j in range(N)])
    rho = r / denom if denom > 0 else np.zeros(N)
    return list(range(N)), rho.tolist()

def normalized_cross_correlation_periodic(x1, x2):
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)
    N = max(len(x1), len(x2))
    return normalized_cross_correlation(np.resize(x1, N), np.resize(x2, N))

def time_delay(x1, x2, Ts):
    lags, rho = normalized_cross_correlation_periodic(x1, x2)
    lag = int(np.argmax(rho))
    return lag * float(Ts), lag