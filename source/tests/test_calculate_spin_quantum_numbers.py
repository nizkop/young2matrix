from source.pure_chemical_functions.calculate_ms_quantum_number import calculate_ms_quantum_number
from source.pure_chemical_functions.calculate_spin_quantum_numbers import calculate_spin_quantum_numbers



trials = [
    {"input": 2, "expected": [0, 1], "error_message": "S3: wrong calculation of total spin choices"},
    {"input": 3, "expected": [1/2, 3/2], "error_message": "S3: wrong calculation of total spin choices"},
    {"input": 4, "expected": [0, 1, 2], "error_message": "S4: wrong calculation of total spin choices"},
    # {"input": [], "expected": , "error_message": ""},
]
for i in trials:
    actual = calculate_spin_quantum_numbers(i["input"])
    if not sorted(actual) == sorted(i["expected"]) :
        raise Exception(i["error_message"]+f": {actual} vs. {i['expected']}" )







trials = [
        {"input": 0, "expected": [0], "error_message": "total spin = 0, ms wrong"},
        {"input": 1/2, "expected": [-1/2, 1/2], "error_message": "total spin = 1/2, ms wrong"},
        {"input": 1, "expected": [-1,0,1], "error_message": "total spin = 1, ms wrong"},
        {"input": 2, "expected": [-2,-1,0,1,2] , "error_message": "total spin = 2, ms wrong"},
        # {"input": , "expected": [], "error_message": ""},
]

for i in trials:
    actual = calculate_ms_quantum_number(i["input"])
    if not sorted(actual) == sorted(i["expected"]):
        raise Exception(i["error_message"] + f": {actual} vs. {i['expected']}")
