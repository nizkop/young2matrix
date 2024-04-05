from source.calculate_spin_quantum_numbers import calculate_spin_quantum_numbers

trials = [
    {"input": 2, "expected": [0, 1], "error_message": "S3: wrong calculation of total spin choices"},
    {"input": 3, "expected": [1/2, 3/2], "error_message": "S3: wrong calculation of total spin choices"},
    {"input": 4, "expected": [0, 1, 2], "error_message": "S4: wrong calculation of total spin choices"},
    # {"input": [], "expected": , "error_message": ""},
]
for i in trials:
    expected = i["expected"]
    actual = calculate_spin_quantum_numbers(i["input"])
    if not actual == expected :
        raise Exception(i["error_message"]+f": {actual} vs. {expected}" )