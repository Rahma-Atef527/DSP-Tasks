def sub_signal(signal1, signal2):
    if len(signal1) != len(signal2):
        raise ValueError("Signals must have the same number of samples")
    res = []
    for i in range(len(signal1)):
        res.append(signal1[i] - signal2[i])
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

def accumulate_signeal(signal):
    res = []
    total = 0

    for val in signal:
        total += val
        res.append(total)

    return res