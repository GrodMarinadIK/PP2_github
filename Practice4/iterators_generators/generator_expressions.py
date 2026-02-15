# List comprehension - creates the entire list in memory
list_comp = [x * x for x in range(5)]

# Generator expression - creates an object that generates values on the fly
# (Uses parentheses instead of square brackets)
gen_exp = (x * x for x in range(5))

print(list_comp)
print(gen_exp) # Will print the generator object, not the values

# Efficiently using generator expression with built-in functions
total = sum(x * x for x in range(10))
print(total)