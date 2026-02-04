##################################################################################################
# Тема: *args, **kwargs, combination with usuual parameteres, Argument unpacking (* и **).
##################################################################################################

def sum_all(*numbers: float) -> float:
    total = 0.0
    for n in numbers:
        total += n
    return total


def max_value(*numbers: float):
    if len(numbers) == 0:
        return None
    m = numbers[0]
    for n in numbers:
        if n > m:
            m = n
    return m


def print_user(username: str, **details) -> None:
    print("Username:", username)
    if not details:
        print("No additional details")
        return
    print("Additional details:")
    for k, v in details.items():
        print(f"  {k}: {v}")


def debug_call(title: str, *args, **kwargs) -> None:
    print("Title:", title)
    print("Positional args:", args)
    print("Keyword args:", kwargs)


def add_three(a: int, b: int, c: int) -> int:
    return a + b + c


def greet_person(fname: str, lname: str) -> str:
    return f"Hello {fname} {lname}"


if __name__ == "__main__":
    print(sum_all(1, 2, 3))
    print(sum_all(10, 20, 30, 40))
    print(max_value(3, 7, 2, 9, 1))
    print(max_value())

    print_user("emil123", age=25, city="Oslo", hobby="coding")
    print_user("no_details_user")

    debug_call("User Info", "Gumball", "Strassen", age=25, city="Oslo")

    nums = [1, 2, 3]
    print(add_three(*nums))

    person = {"fname": "Emil", "lname": "Refsnes"}
    print(greet_person(**person))
