##################################################################################################
# Topic: What is lambda, 1 expression, any amount of arguments, lambda as "anonym",
# lambda in a function (замыкание / factory).
##################################################################################################

def make_multiplier(n: int):
    """
    Return a function, which multiplies input by n.
    Example: doubler = make_multiplier(2); doubler(11) -> 22
    """
    return lambda a: a * n


def make_power(p: int):
    """Returns a fucntion, which raises number to the power p."""
    return lambda x: x ** p


def apply_twice(func, x):
    """Takes a function and applies it TWICE."""
    return func(func(x))


if __name__ == "__main__":
    # 1) Basic form
    add_10 = lambda a: a + 10
    print(add_10(5))  # 15

    # 2) Several arguments
    mul = lambda a, b: a * b
    print(mul(5, 6))  # 30

    # 3) 3 arguments
    summ = lambda a, b, c: a + b + c
    print(summ(5, 6, 2))  # 13

    # 4) lambda in a fucntion: factory
    doubler = make_multiplier(2)
    tripler = make_multiplier(3)
    print(doubler(11))  # 22
    print(tripler(11))  # 33

    square = make_power(2)
    cube = make_power(3)
    print(square(7))  # 49
    print(cube(4))    # 64

    # 5) lambda as an argument into a function (короткий одноразовый коллбек)
    print(apply_twice(lambda x: x + 1, 10))  # 12
    print(apply_twice(lambda x: x * 2, 5))   # 20
