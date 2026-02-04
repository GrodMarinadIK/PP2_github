##############################################################################################
# Theme: return, multiple returns, default None, return different types, early terminating (loop).
##############################################################################################

def get_greeting() -> str:
    return "Hello from a function"


def add(x: float, y: float) -> float:
    return x + y


def safe_divide(a: float, b: float):
    """returns None, if division is impossible."""
    if b == 0:
        return None
    return a / b


def min_max(values: list[int]) -> tuple[int, int] | None:
    """returns (min, max) or None for empty list."""
    if not values:
        return None
    return (min(values), max(values))


def build_person(name: str, age: int) -> dict:
    return {"name": name, "age": age}


def list_fruits() -> list[str]:
    return ["apple", "banana", "cherry"]


def first_positive(nums: list[int]) -> int | None:
    """Early return: found first positive — returned."""
    for x in nums:
        if x > 0:
            return x
    return None


if __name__ == "__main__":
    print(get_greeting())
    print(add(5, 3))

    print(safe_divide(10, 2))
    print(safe_divide(10, 0))

    print(min_max([3, 7, 2, 9, 1]))
    print(min_max([]))

    print(build_person("Lina", 24))
    fruits = list_fruits()
    print(fruits, fruits[0])

    print(first_positive([-5, -2, 0, 4, 10]))
    print(first_positive([-5, -2, 0]))
