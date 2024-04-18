from source.chemical_standard_tableau import chemical_standard_tableau


trials = [
        {"input":  [(1 ,2 ,3)],
         "expected":  [ {"total_spin": 3/2, "ms": 3/2}, {"total_spin": 3/2, "ms": 1/2},
                        {"total_spin": 3/2, "ms": -1/2}, {"total_spin": 3/2, "ms": -3/2} ],
         "error_message": "S3 total symmetric"},
        {"input": [(1,2),(3,)],
         "expected": [{"total_spin": 1/2, "ms": 1/2},{"total_spin": 1/2, "ms": -1/2}],
         "error_message": "S3 antisymmetric in 3"},
        {"input": [(1, 3), (2,)],
         "expected": [{"total_spin": 1 / 2, "ms": 1 / 2}, {"total_spin": 1 / 2, "ms": -1 / 2}],
         "error_message": "S3 antisymmetric in 2"},
        {"input": [(1,),(2,), (3,)], "expected": [],
         "error_message": "S3 antisymmetric in 1,2,3"},

        {"input": [(1, 2, 3, 4)],
         "expected": [{"total_spin": 2, "ms": 2}, {"total_spin": 2, "ms": 1},{"total_spin": 2, "ms": 0},
                      {"total_spin": 2, "ms": -1}, {"total_spin": 2, "ms": -2}],
         "error_message": "S4 total symmetric"},
        {"input": [(1, 2, 3),(4,)],
         "expected": [{"total_spin": 1, "ms": 1}, {"total_spin": 1, "ms": 0}, {"total_spin": 1, "ms": -1 }],
         "error_message": "S4 antisymmetric 4"},
        {"input": [(1, 3, 4), (2,)],
         "expected": [{"total_spin": 1, "ms": 1}, {"total_spin": 1, "ms": 0}, {"total_spin": 1, "ms": -1}],
         "error_message": "S4 antisymmetric 2"},
        {"input": [(1, 2, 4), (3,)],
         "expected": [{"total_spin": 1, "ms": 1}, {"total_spin": 1, "ms": 0}, {"total_spin": 1, "ms": -1}],
         "error_message": "S4 antisymmetric 3"},
        {"input": [(1, 2,), (3, 4)],
         "expected": [{"total_spin": 0, "ms": 0}],
         "error_message": "S4 2x2"},
        {"input": [(1, 3,), (2, 4)],
         "expected": [{"total_spin": 0, "ms": 0}],
         "error_message": "S4 2x2"},
        # {"input": , "expected": [], "error_message": ""},
]



general_error = "error in getting spin functions"
for i in trials:
    s = chemical_standard_tableau(i["input"])
    s.set_up_function()
    s.get_spin_choices()

    calculated_values = []
    for t in s.spin_parts:
        calculated_values.append({"total_spin": t.total_spin, "ms": t.ms})

    for should_be in i["expected"]:
        if should_be not in calculated_values:
            raise Exception(general_error + " - missing function - " + i["error_message"])

    for should_be in calculated_values:
        if should_be not in i["expected"]:
            raise Exception(general_error + " - to many functions - " + i["error_message"])
