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