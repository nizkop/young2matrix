from source.function_parts.sign import Sign
from source.standard_tableau import standard_tableau

# ! these tests are sensitive to the order of summands (= an error might not be a mistake)
trials = [
    # # single operators:
    # {"input": [(1, 2)], "expected": ["+a1b2", "+a2b1"], "error_message": "symmetrizing wrong"},
    # {"input": [(1,),(2,)], "expected": ["+a1b2", "-a2b1"], "error_message": "anti-symmetrizing wrong"},
    # {"input": [(1,2,3)], "expected": ["+a1b2c3","+a1b3c2","+a2b1c3", "+a2b3c1", "+a3b1c2", "+a3b2c1"], "error_message": "symmetrizing wrong (> 2)"},
    # {"input": [(1,),(2,),(3,)], "expected": ["+a1b2c3","-a1b3c2", "-a2b1c3", "+a2b3c1", "+a3b1c2", "-a3b2c1"], "error_message": "anti-symmetrizing wrong (> 2)"},
    # # mixed terms:
    # {"input": [(1,2),(3,)], "expected": ["+a1b2c3", "-a3b2c1", "+a2b1c3" , "-a2b3c1"], "error_message": "anti- & symmetrizing wrong"},
    # {"input": [(1,3),(2,)], "expected": ["+a1b2c3", "-a2b1c3", "-a3b1c2" , "+a3b2c1"], "error_message": "anti- & symmetrizing wrong"},

    {"input": [(1,2),(3,4)],
     "expected": {"a1b2c3d4":Sign.PLUS, "a2b1c3d4": Sign.PLUS, "a1b2c4d3": Sign.PLUS, "a2b1c4d3": Sign.PLUS ,
                  "a3b2c1d4": Sign.MINUS , "a2b3c1d4": Sign.MINUS , "a3b2c4d1": Sign.MINUS , "a2b3c4d1": Sign.MINUS ,
                  "a1b4c3d2": Sign.MINUS , "a4b1c3d2": Sign.MINUS , "a1b4c2d3": Sign.MINUS, "a4b1c2d3": Sign.MINUS,
                  "a3b4c1d2": Sign.PLUS, "a4b3c1d2": Sign.PLUS, "a3b4c2d1": Sign.PLUS, "a4b3c2d1": Sign.PLUS},
     "error_message": "S4"
     }
    # {"input": [], "expected": "+ ", "error_message": ""},
]


for i in trials:
    expected = i["expected"]
    s = standard_tableau(i["input"])
    s.set_up_function()

    if not s.function.get_number_of_terms() == len(i["expected"].keys()):
        raise Exception("wrong number of terms: "+i["error_message"])
    for p in s.function.parts:
        # print()
        actual = p.to_text().replace("* ","").replace("_","").replace(" ","").replace('-',"")
        # print(actual)
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
        # try:
        #     index = [y.replace("−", "").replace("-","").replace("+","") for y in expected].index(actual)
        # except ValueError:
        #     print( [y.replace("−", "").replace("-","").replace("+","") for y in expected] )
        #     raise Exception(i["error_message"] + f": {[actual]} vs. {[y.replace('−','') for y in expected]}")
        #
        # if sign == "+":
        #     if sign not in expected[index]:
        #         raise Exception(i["error_message"] + f": wrong sign for {actual}, {i['error_message']}")
        # else:
        #     if "+" in expected[index]:
        #         raise Exception(i["error_message"] + f": wrong sign for {actual}, {i['error_message']}")



    # actual = s.function.to_text().replace(" ","").replace("*","")
    # if not actual == expected.replace(" ","").replace("*","") :
    #     raise Exception(i["error_message"]+": "+ actual+ " vs. "+ expected)


