# Boolean values are: True or False

# Sometimes you need to know if expression is True or False
# Python can do this for you

print(bool("Hello World"))
print(bool(15))

#
print()
#

# Most values are True if they have content 
print(bool("abcd"))
print(bool(542))
print(bool(['bananae', 'Kokshetau', 'PC']))

#
print()
#

# Some values are False - usually: empty values, 0, None, and False
print(bool(False))
print(bool(0))
print(bool(None))
print(bool(""))
print(bool(''))
print(bool({}))
print(bool([]))
print(bool( () ))

#
print()
#

# Special case for False: objects with __len__ returning 0
class myclass():
    def __len__(self):
        return 0

my_object = myclass()
print(bool(my_object))
