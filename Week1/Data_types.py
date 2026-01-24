# All datatypes...

# Text types:
x = str("Namaste, world")
print(f"x = {x}, type of x = {type(x)}")

# Numeric types:
num1 = int(206)
num2 = float(95.1)
num3 = complex(2 + 1j)
print(f"num1 = {num1}, type of num1 = {type(num1)}")
print(f"num2 = {num2}, type of num2 = {type(num2)}")
print(f"num3 = {num3}, type of num3 = {type(num3)}")

# Sequence Types:
List = list(('banana', 'gaming mouse', 'match'))
Tuple = tuple(('rubber', 'Sprite', 'match'))
Range = range(0, 10, -1)
print(f"List = {List}, type of List = {type(List)}")
print(f"Tuple = {Tuple}, type of Tuple = {type(Tuple)}")
print(f"Range = {Range}, type of Range = {type(Range)}")

# Mapping types:
Dict = dict(name="Lev", age=18)
print(f"Dict = {Dict}, type of Dict = {type(Dict)}")

# Set types:
Set = set(("banana", "banana", "apple", "grape"))
Frozenset = frozenset(("banana", "banana", "apple", "grape"))
print(f"Set = {Set}, type of Set = {type(Set)}")
print(f"Frozenset = {Frozenset}, type of Frozenset = {type(Frozenset)}")

# Boolean type
Boolean = bool(5)
print(f"Boolean = {Boolean}, type of Boolean = {type(Boolean)}")

# Binary Types:
Bytes = bytes(25)
Bytearray = bytearray(25)
MemoryView = memoryview(bytes(25))
print(f"Bytes = {Bytes}, type of Bytes = {type(Bytes)}")
print(f"Bytearray = {Bytearray}, type of Bytearray = {type(Bytearray)}")
print(f"MemoryView = {MemoryView}, type of MemoryView = {type(MemoryView)}")

# NoneType:
Nonetype = None
print(f"Nonetype = {Nonetype}, type of Nonetype = {type(Nonetype)}")

