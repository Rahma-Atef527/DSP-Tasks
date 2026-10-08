#test code
def ReadSignalFile(file_name):

    expected_indices = []
    expected_samples = []

    with open(file_name, "r") as f:

        # Skip first 3 header lines
        f.readline()
        f.readline()
        f.readline()

        line = f.readline()

        while line:

            L = line.strip()

            if not L:
                line = f.readline()
                continue

            parts = L.split()

            if len(parts) >= 2:

                V1 = int(parts[0])
                V2 = float(parts[1])

                expected_indices.append(V1)
                expected_samples.append(V2)

                line = f.readline()

            else:
                break

    return expected_indices, expected_samples


# =========================================================
# ADDITION TEST
# =========================================================

def AddSignalSamplesAreEqual(
    userFirstSignal,
    userSecondSignal,
    Your_indices,
    Your_samples
):

    if (
        userFirstSignal == "Signal1.txt"
        and userSecondSignal == "Signal2.txt"
    ):

        file_name = "Signal1+signal2.txt"

    elif (
        userFirstSignal == "Signal1.txt"
        and userSecondSignal == "Signal3.txt"
    ):

        file_name = "signal1+signal3.txt"

    else:

        print("Unsupported signal combination.")
        return

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            "Addition Test case failed, "
            "your signal has different length from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                "Addition Test case failed, "
                "your signal has different indices from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue

        else:

            print(
                "Addition Test case failed, "
                "your signal has different values from the expected one"
            )

            return

    print("Addition Test case passed successfully")


# =========================================================
# MULTIPLICATION TEST
# =========================================================

def MultiplySignalByConst(
    User_Const,
    Your_indices,
    Your_samples
):

    if User_Const == 5:

        file_name = "MultiplySignalByConstant-Signal1 - by 5.txt"

    elif User_Const == 10:

        file_name = "MultiplySignalByConstant-signal2 - by 10.txt"

    else:

        print("Unsupported constant.")
        return

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            "Multiply by "
            + str(User_Const)
            + " Test case failed, "
            "your signal has different length from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                "Multiply by "
                + str(User_Const)
                + " Test case failed, "
                "your signal has different indices from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue

        else:

            print(
                "Multiply by "
                + str(User_Const)
                + " Test case failed, "
                "your signal has different values from the expected one"
            )

            return

    print(
        "Multiply by "
        + str(User_Const)
        + " Test case passed successfully"
    )


# =========================================================
# GENERAL SIGNAL TEST
# =========================================================

def SignalSamplesAreEqual(
    TaskName,
    output_file_name,
    Your_indices,
    Your_samples
):

    expected_indices = []
    expected_samples = []

    with open(output_file_name, "r") as f:

        # Skip first 3 header lines
        f.readline()
        f.readline()
        f.readline()

        line = f.readline()

        while line:

            L = line.strip()

            if not L:
                line = f.readline()
                continue

            parts = L.split()

            if len(parts) >= 2:

                V1 = int(parts[0])
                V2 = float(parts[1])

                expected_indices.append(V1)
                expected_samples.append(V2)

                line = f.readline()

            else:
                break

    if (
        len(expected_samples) != len(Your_samples)
        or len(expected_indices) != len(Your_indices)
    ):

        print(
            TaskName
            + " Test case failed, "
            "your signal has different length from the expected one"
        )

        return

    for i in range(len(Your_indices)):

        if Your_indices[i] != expected_indices[i]:

            print(
                TaskName
                + " Test case failed, "
                "your signal has different indices from the expected one"
            )

            return

    for i in range(len(expected_samples)):

        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue

        else:

            print(
                TaskName
                + " Test case failed, "
                "your signal has different values from the expected one"
            )

            return

    print(
        TaskName
        + " Test case passed successfully"
    )