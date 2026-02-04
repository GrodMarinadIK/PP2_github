##############################################################################################
# Theme: позиционные/ключевые аргументы, значения по умолчанию, 
# / и * (positional-only и keyword-only), смешивание positional + keyword.
##############################################################################################

def full_name(first: str, last: str) -> str:
    return f"{first} {last}"


def hello(name: str = "friend") -> None:
    print("Hello", name)


def describe_pet(animal: str, name: str) -> str:
    return f"I have a {animal}. My {animal}'s name is {name}."


def order_price(item: str, quantity: int = 1, price_per_unit: float = 0.0) -> float:
    return quantity * price_per_unit


def pos_only_example(name, /) -> str:
    # name можно передать только позиционно
    return f"Hello {name}"


def kw_only_example(*, name: str) -> str:
    # name можно передать только ключом
    return f"Hello {name}"


def mixed_example(a, b, /, *, c, d) -> int:
    # a,b - positional-only; c,d - keyword-only
    return a + b + c + d


if __name__ == "__main__":
    print(full_name("Khidir", "Karawita"))
    hello("Ismail Ahmad Kanabawi")
    hello()

    print(describe_pet("cat", "Usman Abdul Jalil Sisha"))
    print(describe_pet(name="Odie", animal="dog"))

    print(order_price("brick", quantity=67, price_per_unit=52))

    print(pos_only_example("Damir"))
    # pos_only_example(name="Damir")  # TypeError

    print(kw_only_example(name="Ariel"))
    # kw_only_example("Ariel")  # TypeError

    print(mixed_example(5, 10, c=15, d=20))
