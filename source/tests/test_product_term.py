from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign

p1 = product_term(Sign("+"), ordered_functions=(1, 2))
p1.factor = 5
p2 = product_term(Sign("+"), ordered_functions=(1, 3))
p2.factor = 3

trials = [
        {"input1": product_term(Sign("+"), ordered_functions=(2, 1)),
         "input2":  product_term(Sign("+"), ordered_functions=(1, 2)),
         "expected": {"factor": 1, "list_of_parts": ['a_{1}', 'b_{2}', 'a_{2}', 'b_{1}']},
         "error_message": "S2: different functions"},
        {"input1": product_term(Sign("+"), ordered_functions=(2, 1)),
         "input2":  product_term(Sign("+"), ordered_functions=(2, 1)),
         "expected": {"factor": 1, "list_of_parts": ['a_{2}^{2}', 'b_{1}^{2}']},
         "error_message": "S2: ab multiplying itself"},
        {"input1": product_term(Sign("+"), ordered_functions=(1, 2)),
         "input2": product_term(Sign("+"), ordered_functions=(1, 2)),
         "expected": {"factor": 1, "list_of_parts": ['a_{1}^{2}', 'b_{2}^{2}']},
         "error_message": "S2: ba multiplying itself"},
        {"input1": p1,
         "input2": p2,
         "expected": {"factor": 15, "list_of_parts": ['a_{1}^{2}', 'b_{2}', 'b_{3}']},
         "error_message": "S2: multiplying itself"},
        # {"input": , "expected": [], "error_message": ""},
]

general_error = "error in getting product term"
for i in trials:
    calculated = i["input1"].multiply(i["input2"])
    if calculated.factor != i["expected"]["factor"]:
        raise Exception(f"{general_error} - {i['error_message']}: wrong numeral factor")
    if sorted(calculated.get_list_of_parts()) != sorted(i["expected"]["list_of_parts"]):
        raise Exception(f"{general_error} - {i['error_message']}: wrong functional factors")




###  overlap spatial  ###

trials = [
    {"input1": product_term(Sign("+"), (1, 2)),"input2":product_term(Sign("+"), ordered_functions=(1,2)),
     "expected": 1, "error_message": "S2: multiplying itself"},
    {"input1": product_term(Sign("+"), (1, 2)), "input2": product_term(Sign("+"), ordered_functions=(2,1)),
     "expected": 0, "error_message": "S2: multiplying antisymmetric"},
    {"input1": product_term(Sign("+"), (1, 2, 3)), "input2": product_term(Sign("-"), ordered_functions=(3,2,1)),
     "expected": 0, "error_message": "S3"},
]

general_error = "building overlap"
for trial in trials:
    calculated, eq = trial["input1"].integrational_multiply(trial["input2"])

    if calculated.factor != trial["expected"]:
        raise Exception(f"{general_error}: {trial['error_message']}")

###  overlap spin  ###
trials = [
    {"input1": product_term(Sign("+"), ordered_functions=(1, 2)), "spin1": ["α", "β"],
     "input2": product_term(Sign("+"), ordered_functions=(1, 2)), "spin2": ["α", "β"],
     "expected": 1, "error_message": "S2: multiplying itself"},
    {"input1": product_term(Sign("+"), ordered_functions=(1, 2)), "spin1": ["α", "β"],
     "input2": product_term(Sign("+"), ordered_functions=(1, 2)), "spin2": ["β", "α"],
     "expected": 0, "error_message": "S2: multiplying itself with switched spins"},
    {"input1": product_term(Sign("+"), (1, 2)),  "spin1": ["α", "β"],
     "input2": product_term(Sign("+"), ordered_functions=(2, 1)),  "spin2": ["α", "β"],
     "expected": 0, "error_message": "S2: multiplying antisymmetric"},
    {"input1": product_term(Sign("+"), (1, 2)), "spin1": ["β", "α"],
     "input2": product_term(Sign("+"), ordered_functions=(2, 1)), "spin2": ["α", "β"],
     "expected": 1, "error_message": "S2: multiplying antisymmetric with switched spin"},
]

general_error = "building overlap for spin functions"
for trial in trials:
    p1 = trial["input1"]
    p2 = trial["input2"]
    p1.lowercase_letters = trial["spin1"]
    p2.lowercase_letters = trial["spin2"]

    calculated, eq = p1.integrational_multiply(p2)
    # print(eq, "=", calculated.to_text())
    if calculated.factor != trial["expected"]:
        raise Exception(f"{general_error}: {trial['error_message']}")