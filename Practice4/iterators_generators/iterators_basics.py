# Basic iterables: tuples and strings
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple) # Get an iterator object

print(next(myit)) # Output: apple
print(next(myit)) # Output: banana
print(next(myit)) # Output: cherry

# Strings are also iterable objects
mystr = "banana"
myit_str = iter(mystr)
print(next(myit_str)) # Output: b

# A 'for' loop internally creates an iterator and calls next()
for x in mytuple:
    print(x)
    
# --- WHAT A 'FOR' LOOP DOES UNDER THE HOOD ---
'''

mytuple = ("apple", "banana", "cherry")

# 1. Manual simulation of a 'for' loop:
iterator_obj = iter(mytuple) # Get the iterator

while True:
    try:
        # 2. Get the next item
        item = next(iterator_obj)
        print(item)
    except StopIteration:
        # 3. If StopIteration is raised, break the loop
        break

# This code above is logically identical to:
# for x in mytuple:
#     print(x)

'''