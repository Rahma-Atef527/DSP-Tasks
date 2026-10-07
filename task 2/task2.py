import math

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

def quantize_signal(signal, levels = None, bits = None):
    if len(signal) == 0:
        return [], [], [], 0
    if bits is not None:
        if bits < 1:
            raise ValueError("bits must be at least 1")
        levels = 2 ** bits
    elif levels is not None:
        if levels < 2:
            raise ValueError("levels must be at least 2")
        bits = math.ceil(math.log2(levels))
    else:
        raise ValueError("enter levels or bits")

    min_val = min(signal)
    max_val = max(signal)
    if max_val == min_val:
        raise ValueError("constant signal cannot be quantized")
    delta = (max_val - min_val) / levels
    quantized = []
    errors = []
    encoded = []

    for val in signal:
        index = int((val - min_val) / delta)
        if index >= levels:
            index = levels - 1

        mid = min_val + delta * (index + 0.5)
        quantized.append(mid)
        errors.append(mid - val)
        encoded.append(format(index, "0" + str(bits) + "b"))

    return quantized, errors, encoded, bits