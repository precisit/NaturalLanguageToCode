def generate_code(objects, actions):
    """Generate Code docstring"""
    code_string = ""
    for action in actions:
        is_conditional = False
        is_loop = False
        if action.condition is not None:
            code_string += str(action.condition) + ": \n"
            is_conditional = True
        if action.loop_iterations > 1:
            is_loop = True
            if is_conditional:
                code_string += "\t"
            code_string += "for i in range(0," + str(action.loop_iterations) + "): \n"
        if is_conditional:
            code_string += "\t"
        if is_loop:
            code_string += "\t"
        if action.on_object is not None and action.on_object.isValid:
            code_string += action.on_object.name + "."
        code_string += action.name + "("
        if len(action.parameters) > 0:
            if "target" in action.parameters:
                # the string "target.position"" or the actual position of the object?
                if action.parameters["target"] in objects:
                    code_string += action.parameters["target"].name + ", "
                elif action.parameters["target"] is not None:
                    code_string += action.parameters["target"] + ", "
            if "with" in action.parameters:
                if action.parameters["with"] in objects:
                    code_string += action.parameters["with"].name +", "
                elif action.parameters["with"] is not None:
                    code_string += action.parameters["with"] +", "
            if "direction" in action.parameters:
                code_string += action.parameters["direction"] + ", "
            if "how" in action.parameters:
                code_string += action.parameters["how"] + ", "

        code_string = code_string.rstrip(', ')
        code_string += ") \n"

    return code_string
