from fractions import Fraction

from source.ChemicalStandardTableau import ChemicalStandardTableau

###   testing found functions in ChemicalStandardTableau   ###

trials = [
        # weissbluth examples:
        {"input":  [(1 ,2 ,3)],
             "expected":  [ {"total_spin": Fraction(3,2), "ms": Fraction(3,2), "behavior": [['α1', 'α2', 'α3']]},
                            {"total_spin": Fraction(3,2), "ms": Fraction(1,2), "behavior": [['α1', 'α2', 'β3'], ['α1', 'α3', 'β2'], ['α2', 'α3', 'β1']]},
                            {"total_spin": Fraction(3,2), "ms": -Fraction(1,2), "behavior": [['β1', 'β2', 'α3'], ['β1', 'β3', 'α2'], ['β2', 'β3', 'α1']]},
                            {"total_spin": Fraction(3,2), "ms": -Fraction(3,2), "behavior": [['β1', 'β2', 'β3']]}
                            ],
             "error_message": "S3 total symmetric"},
        {"input": [(1,2),(3,)],
             "expected": [{"total_spin": Fraction(1,2), "ms": Fraction(1,2), "behavior": [['α1', 'α2', 'β3'], ['β1', 'α2', 'α3']]},
                          {"total_spin": Fraction(1,2), "ms": -Fraction(1,2), "behavior": [['α1', 'β2', 'β3'], ['β1', 'β2', 'α3']]} ],
             "error_message": "S3 antisymmetric in 3"},
        {"input": [(1, 3), (2,)],
             "expected": [{"total_spin": Fraction(1, 2), "ms": Fraction(1, 2), "behavior": [['α1', 'β2', 'α3'], ['β1', 'α2', 'α3']]},
                          {"total_spin": Fraction(1, 2), "ms": -Fraction(1, 2), "behavior": [['α1', 'β2', 'β3'], ['β1', 'α2', 'β3']]} ],
             "error_message": "S3 antisymmetric in 2"},
        {"input": [(1,),(2,), (3,)], "expected": [],
             "error_message": "S3 antisymmetric in 1,2,3"},

        # manually calculated examples:
        {"input": [(1, 2, 3, 4)],
             "expected": [{"total_spin": 2, "ms": 2 , "behavior": [['α1', 'α2', 'α3', 'α4']] },
                          {"total_spin": 2, "ms": 1 , "behavior": [['α1', 'α2', 'α3', 'β4'], ['α1', 'α2', 'β3', 'α4'], ['α1', 'β2', 'α3', 'α4'], ['β1', 'α2', 'α3', 'α4']] },
                          {"total_spin": 2, "ms": 0 ,
                           "behavior": [['α1', 'α2', 'β3', 'β4'], ['α1', 'β2', 'α3', 'β4'], ['β1', 'α2', 'α3', 'β4'],
                                        ['β1', 'α2', 'β3', 'α4'], ['α1', 'β2', 'β3', 'α4'], ['β1', 'β2', 'α3', 'α4'] ] },
                          {"total_spin": 2, "ms": -1, "behavior": [['β1', 'β2', 'β3', 'α4'], ['β1', 'β2', 'α3', 'β4'], ['β1', 'α2', 'β3', 'β4'], ['α1', 'β2', 'β3', 'β4']] },
                          {"total_spin": 2, "ms": -2, "behavior": [['β1', 'β2', 'β3', 'β4']] }],
             "error_message": "S4 total symmetric"},
        {"input": [(1, 2, 3),(4,)],
             "expected": [{"total_spin": 1, "ms": 1 , "behavior": [['α1', 'α2', 'α3', 'β4'], ['β1', 'α2', 'α3', 'α4']] },
                          {"total_spin": 1, "ms": 0 ,
                           "behavior": [['α1', 'α2', 'β3', 'β4'], ['α1', 'β2', 'α3', 'β4'],
                                        ['β1', 'α2', 'β3', 'α4'], ['β1', 'β2', 'α3', 'α4'] ] },
                          {"total_spin": 1, "ms": -1, "behavior": [['α1', 'β2', 'β3', 'β4'], ['β1', 'β2', 'β3', 'α4'] ] }],
             "error_message": "S4 antisymmetric 4"},
        {"input": [(1, 3, 4), (2,)],
             "expected": [{"total_spin": 1, "ms": 1 , "behavior": [['α1', 'β2', 'α3', 'α4'], ['β1', 'α2', 'α3', 'α4']] },
                          {"total_spin": 1, "ms": 0 ,
                           "behavior": [['α1', 'β2', 'α3', 'β4'], ['β1', 'α2', 'α3', 'β4'],
                                        ['α1', 'β2', 'β3', 'α4'], ['β1', 'α2', 'β3', 'α4']] },
                          {"total_spin": 1, "ms": -1, "behavior": [['α1', 'β2', 'β3', 'β4'], ['β1', 'α2', 'β3', 'β4'] ] }],
             "error_message": "S4 antisymmetric 2"},
        {"input": [(1, 2, 4), (3,)],
             "expected": [{"total_spin": 1, "ms": 1 , "behavior": [['α1', 'α2', 'β3', 'α4'], ['β1', 'α2', 'α3', 'α4']] },
                          {"total_spin": 1, "ms": 0 , "behavior": [['α1', 'α2', 'β3', 'β4'], ['β1', 'α2', 'α3', 'β4'],
                                                                   ['α1', 'β2', 'β3', 'α4'], ['β1', 'β2', 'α3', 'α4']] },
                          {"total_spin": 1, "ms": -1, "behavior": [['α1', 'β2', 'β3', 'β4'], ['β1', 'β2', 'α3', 'β4'] ] }],
             "error_message": "S4 antisymmetric 3"},
        {"input": [(1, 2,), (3, 4)],
             "expected": [{"total_spin": 0, "ms": 0, "behavior": [['α1', 'α2', 'β3', 'β4'], ['β1', 'α2', 'α3', 'β4'],
                                                                  ['α1', 'β2', 'β3', 'α4'], ['β1', 'β2', 'α3', 'α4']] }],
             "error_message": "S4 2x2"},
        {"input": [(1, 3,), (2, 4)],
             "expected": [{"total_spin": 0, "ms": 0, "behavior": [['α1', 'β2', 'α3', 'β4'], ['β1', 'α2', 'α3', 'β4'],
                                                                  ['α1', 'β2', 'β3', 'α4'], ['β1', 'α2', 'β3', 'α4']] }],
             "error_message": "S4 2x2"},
]

general_error = "error in getting spin functions"
for i in trials:
    s = ChemicalStandardTableau(i["input"])
    s.set_up_function()
    s.get_spin_choices()

    # getting calculated information:
    calculated_values = []
    for t in s.spin_parts:
        calculated_values.append({"total_spin": t.total_spin, "ms": t.ms, "behavior": []})
        for term in t.function.parts:
            term_parts = [f.replace("{","").replace("}","").replace("_","") for f in term.get_list_of_parts()]
            term_parts.sort()
            calculated_values[-1]["behavior"].append(term_parts)
        calculated_values[-1]["behavior"].sort()

    # checking:
    for should_be in i["expected"]:
        for term in should_be["behavior"]:
            term.sort()
        should_be["behavior"].sort()
        assert should_be in calculated_values, f"{general_error} - missing function - {i['error_message']}"
        #<- compares whole dict (spin + ms + behavior) (<- thereby sorting needed before)

    assert len(calculated_values) == len(i["expected"]), f"{general_error} - to many functions - {i['error_message']}"
    # ! does not check sign for the different product term parts in the different spin combinations

