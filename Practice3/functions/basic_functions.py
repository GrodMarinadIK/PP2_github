##################################################################################################
# Theme: What is a function, how to declare, how to call, docstring, pass, reuse.
##################################################################################################

def say_hello() -> None:
    """Printing a greeting."""
    print("Hello from a function")


def greet(name: str) -> None:
    """Printing a personal greeting."""
    print(f"Hello, {name}!")


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert temperature: F -> C."""
    return (fahrenheit - 32) * 5 / 9


def is_even(n: int) -> bool:
    """Retruns True, if number is even"""
    return n % 2 == 0


def repeat_text(text: str, times: int) -> str:
    """Repeat a string 'times' times ."""
    return text * times


def placeholder() -> None:
    """If you need to create a function placeholder without any code, use the pass statement"""
    pass


if __name__ == "__main__":
    say_hello()
    greet("Khalid Kashmiri")
    print(fahrenheit_to_celsius(77))
    print(is_even(10), is_even(7))
    print(repeat_text("ha", 3))
    placeholder()
