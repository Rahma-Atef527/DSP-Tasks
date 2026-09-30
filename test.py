from task1 import (
    read_signal,
    add_signal,
    mul_signal,
    plot_continuous,
    plot_discrete,
    plot_two_signals,
    plot_two_discrete_signals
)
# Read signals
signal1 = read_signal("Signal1.txt")
signal2 = read_signal("Signal2.txt")
signal3 = read_signal("signal3.txt")

# Get samples
samples1 = signal1[3]
samples2 = signal2[3]
samples3 = signal3[3]

# Test multiplication
result1 = mul_signal(samples1, 5)

result2 = mul_signal(samples2, 10)


# Test addition
result3 = add_signal([samples1, samples2])

result4 = add_signal([samples1, samples3])


indices1 = signal1[2]
samples1 = signal1[3]

indices2 = signal2[2]
samples2 = signal2[3]

plot_continuous(indices1, samples1)
plot_discrete(indices1, samples1)

plot_two_signals(
    indices1, samples1,
    indices2, samples2
)

plot_two_discrete_signals(
    indices1, samples1,
    indices2, samples2
)

# Print results
print("Signal1 x 5:")
print(result1[:10])

print("\nSignal2 x 10:")
print(result2[:10])

print("\nSignal1 + Signal2:")
print(result3[:10])

print("\nSignal1 + Signal3:")
print(result4[:10])