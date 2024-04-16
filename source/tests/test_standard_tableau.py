from source.standard_tableau import standard_tableau

# ! these tests are sensitive to the order of summands (= an error might not be a mistake)
trials = [
    # single operators:
    {"input": [(1, 2)], "expected": "+ a1 b2 + a2 b1", "error_message": "symmetrizing wrong"},
    {"input": [(1,),(2,)], "expected": "+ a1 b2 - a2 b1", "error_message": "anti-symmetrizing wrong"},
    {"input": [(1,2,3)], "expected": "+ a1b2c3 + a1b3c2 + a2b1c3 + a2b3c1+ a3b1c2 + a3b2c1", "error_message": "symmetrizing wrong (> 2)"},
    {"input": [(1,),(2,),(3,)], "expected": "+ a1b2c3 - a1b3c2 - a2b1c3 + a2b3c1 + a3b1c2 - a3b2c1", "error_message": "anti-symmetrizing wrong (> 2)"},
    # mixed terms:
    {"input": [(1,2),(3,)], "expected": "+ a1b2c3 - a3b2c1 + a2b1c3 - a2b3c1", "error_message": "anti- & symmetrizing wrong"},
    {"input": [(1,3),(2,)], "expected": "+ a1b2c3 - a2b1c3 - a3b1c2 + a3b2c1 ", "error_message": "anti- & symmetrizing wrong"},
    # {"input": [], "expected": "+ ", "error_message": ""},
]


for i in trials:
    expected = i["expected"]
    s = standard_tableau(i["input"])
    s.set_up_function()
    actual = s.function.to_text().replace(" ","").replace("*","")
    if not actual == expected.replace(" ","").replace("*","") :
        raise Exception(i["error_message"]+": "+ actual+ " vs. "+ expected)


