from numpy import (cos, tan,  # type: ignore # noqa: F401
                   sin, sqrt,     # type: ignore # noqa: F401
                   max, min,  # type: ignore # noqa: F401
                   pi, e,  # type: ignore # noqa: F401
                   arcsin, arctan,  # type: ignore # noqa: F401
                   arccos, array,  # type: ignore # noqa: F401
                   ndarray)  # type: ignore # noqa: F401


FUNCTIONS: dict
FUNCTIONS = {"cos": cos, "sin": sin, "tan": tan}


def counter(num_vector: ndarray, constants, functions, pattern, nums_comma, pattern_args):
    nums_comma = int(nums_comma)
    for idx, arg in enumerate(pattern_args):
        if arg in constants:
            pattern = pattern.replace(arg, constants[arg])
        elif arg in functions:
            pattern = pattern.replace(
                arg,
                function_counter(num_vector[idx], functions[arg])
            )
        else:
            pattern = pattern.replace(arg, str(num_vector[idx]))
    return round(
        eval(pattern), nums_comma
        )


def function_counter(num: float, f_name: str):
    return str(
        FUNCTIONS[f_name](num)
               )
