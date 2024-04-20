from source.function_parts.sign import Sign
from source.standard_tableau import standard_tableau


trials = [
    ## examples from weißbluth:
    # single operators:
    {"input": [(1, 2)], "expected": {"a1b2": Sign.PLUS, "a2b1": Sign.PLUS}, "error_message": "symmetrizing wrong"},
    {"input": [(1,),(2,)], "expected": {"a1b2": Sign.PLUS, "a2b1": Sign.MINUS}, "error_message": "anti-symmetrizing wrong"},
    {"input": [(1,2,3)], "error_message": "symmetrizing wrong (> 2)",
     "expected": {"a1b2c3": Sign.PLUS,"a1b3c2": Sign.PLUS,"a2b1c3": Sign.PLUS, "a2b3c1": Sign.PLUS, "a3b1c2": Sign.PLUS, "a3b2c1": Sign.PLUS} },
    {"input": [(1,),(2,),(3,)], "error_message": "anti-symmetrizing wrong (> 2)",
     "expected": {"a1b2c3": Sign.PLUS,"a1b3c2": Sign.MINUS, "a2b1c3": Sign.MINUS, "a2b3c1": Sign.PLUS, "a3b1c2": Sign.PLUS, "a3b2c1": Sign.MINUS}},
    # mixed terms:
    {"input": [(1,2),(3,)], "error_message": "anti- & symmetrizing wrong",
     "expected": {"a1b2c3": Sign.PLUS, "a3b2c1": Sign.MINUS, "a2b1c3": Sign.PLUS , "a2b3c1": Sign.MINUS}},
    {"input": [(1,3),(2,)], "error_message": "anti- & symmetrizing wrong",
     "expected": {"a1b2c3": Sign.PLUS, "a2b1c3": Sign.MINUS, "a3b1c2": Sign.MINUS , "a3b2c1": Sign.PLUS}},

    ## manually calculated: (1. sym, 2. anti)
    {"input": [(1,2),(3,4)],  "error_message": "S4 [2^2] 12-34",
     "expected": {"a1b2c3d4":Sign.PLUS, "a2b1c3d4": Sign.PLUS, "a1b2c4d3": Sign.PLUS, "a2b1c4d3": Sign.PLUS ,
                  "a3b2c1d4": Sign.MINUS, "a2b3c1d4": Sign.MINUS , "a3b2c4d1": Sign.MINUS , "a2b3c4d1": Sign.MINUS ,
                  "a1b4c3d2": Sign.MINUS, "a4b1c3d2": Sign.MINUS , "a1b4c2d3": Sign.MINUS, "a4b1c2d3": Sign.MINUS,
                  "a3b4c1d2": Sign.PLUS, "a4b3c1d2": Sign.PLUS, "a3b4c2d1": Sign.PLUS, "a4b3c2d1": Sign.PLUS}
     },
    {"input": [(1, 3), (2, 4)], "error_message": "S4 [2^2] 13-24",
     "expected": {"a1b2c3d4": Sign.PLUS, "a3b2c1d4": Sign.PLUS, "a1b4c3d2": Sign.PLUS, "a3b4c1d2": Sign.PLUS,
                  "a2b1c3d4": Sign.MINUS, "a3b1c2d4": Sign.MINUS, "a2b4c3d1": Sign.MINUS, "a3b4c2d1": Sign.MINUS,
                  "a1b2c4d3": Sign.MINUS, "a4b2c1d3": Sign.MINUS, "a1b3c4d2": Sign.MINUS, "a4b3c1d2": Sign.MINUS,
                  "a2b1c4d3": Sign.PLUS, "a4b1c2d3": Sign.PLUS, "a2b3c4d1": Sign.PLUS, "a4b3c2d1": Sign.PLUS}
     },
    {"input": [(1,3),(2,),(4,)], "error_message": "S4 [21^1] 13-2-4",
     "expected": {
            "a1b2c3d4": Sign.PLUS , "a2b1c3d4": Sign.MINUS , "a1b4c3d2": Sign.MINUS , "a4b2c3d1": Sign.MINUS, "a2b4c3d1": Sign.PLUS , "a4b1c3d2": Sign.PLUS ,
            "a3b2c1d4": Sign.PLUS , "a3b1c2d4": Sign.MINUS , "a3b4c1d2": Sign.MINUS , "a3b2c4d1": Sign.MINUS , "a3b1c4d2": Sign.PLUS , "a3b4c2d1": Sign.PLUS }
     },
    # {"input": [], "expected": "+ ", "error_message": ""},
]


for i in trials:
    expected = i["expected"]
    s = standard_tableau(i["input"])
    s.set_up_function()

    if not s.function.get_number_of_terms() == len(i["expected"].keys()):
        raise Exception("wrong number of terms: "+i["error_message"])
    for p in s.function.parts:
        actual = p.to_text().replace("* ","").replace("_","").replace(" ","").replace('-',"")
        if "+" in actual:
            sign = Sign.PLUS
            actual = actual.replace("+","")
        else:
            sign = Sign.MINUS
            actual = actual.replace("−", "").replace("-","")

        try:
            if sign != expected[actual]:
                raise Exception(i["error_message"] + f": wrong sign for {actual}, {i['error_message']}")
        except KeyError:
            Exception(i["error_message"] + f": {[actual]} not included in {expected.keys()}")


