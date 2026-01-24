# Strings.
print()
# Those two outputs are the same, so "Pjork" == 'Pjork
print("Pjork")
print('Pjork')

# And that's why we can do like this:
print("That's okayish")
print('"Imagine that this is very mindful quote" © Sum Pёrson')
print("This very fancy machinegun is called '4girl' ")

# Assignment to varaible
s1 = str("Assign me")

# multi-line strings.
poem = """
Roses are red,
Violets are blue;
My dog is my favourite,
but you OK too. """
print(poem)

poem2 = '''
Some flowers are red
Some flowers are pink
Some flowers smell nice
But some flowers stink
'''

# Strings are arrays (of chars) 😲
string_array = "Parivision has beaten Spirit."
print(string_array[3:6])
print()

# Looping through the string.
for x in "Laufey is a great singer":
    print(x, end=" ")
print(); print()

# Length of a string:
lena = "123456789"
print("length of string lena =", len(lena))

# check if substring in a string:
k = "Headshot 2 2 3"
if "Head" in k:
    print("yes, 'Head' is in a string")

if "LA calling" not in k:
    print("No 'La calling' isn't in a string")
    
