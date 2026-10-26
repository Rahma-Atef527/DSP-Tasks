def DerivativeSignal(first_derivative_func, second_derivative_func):
    InputSignal = [float(i) for i in range(1, 101)]

    expectedOutput_first = [1] * 99
    expectedOutput_second = [0] * 98

    # Write your Code here
    indices = list(range(100))

    _, FirstDrev = first_derivative_func(indices, InputSignal)
    _, SecondDrev = second_derivative_func(indices, InputSignal)

    # Testing your Code
    if ((len(FirstDrev) != len(expectedOutput_first)) or
            (len(SecondDrev) != len(expectedOutput_second))):
        print("mismatch in length")
        return

    first = second = True

    for i in range(len(expectedOutput_first)):
        if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
            continue
        else:
            first = False
            print("1st derivative wrong")
            return

    for i in range(len(expectedOutput_second)):
        if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
            continue
        else:
            second = False
            print("2nd derivative wrong")
            return

    if first and second:
        print("Derivative Test case passed successfully")
    else:
        print("Derivative Test case failed")

    return