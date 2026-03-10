from functools import reduce

def run_builtin_exercise():
    # 1. Map and Filter: Data Transformation
    # We start with a list of numbers, square them, and keep only the even ones
    numbers = [1, 2, 3, 4, 5, 6]
    
    # map applies the lambda to every item
    squared = list(map(lambda x: x**2, numbers)) # 1 4 9 16 25 36
    
    # filter keeps only items that satisfy the condition (x % 2 == 0)
    evens = list(filter(lambda x: x % 2 == 0, squared)) # 4 16 36
    
    # 2. Aggregate with reduce: Collapsing data
    # reduce takes the list and "reduces" it to a single cumulative value
    total_sum = reduce(lambda x, y: x + y, evens) # 4 + 16 + 36 = 56
    
    print(f"Original numbers: {numbers}")            #Original numbers: [1, 2, 3, 4, 5, 6]
    print(f"Squared and filtered (evens): {evens}")  #Squared and filtered (evens): [4, 16, 36]
    print(f"Aggregated sum: {total_sum}")            #Aggregated sum: 56

    # 3. Zip and Enumerate: Paired Iteration
    # zip pairs items from two lists, enumerate gives us an index
    names = ["Jiwoo", "Giselle", "Winter"]
    salaries = [5000, 6000, 4500]
    
    print("\n--- Employee Records ---")
    # zip() combines lists into pairs, enumerate() adds a counter
    for index, (name, salary) in enumerate(zip(names, salaries)):
        print(f"#{index + 1}: Name: {name}, Salary: {salary}")
    #--- Employee Records ---
    #1: Name: Jiwoo, Salary: 5000
    #2: Name: Giselle, Salary: 6000
    #3: Name: Winter, Salary: 4500

    # 4. Type Checking and Conversions
    # Checking types and casting data safely
    raw_input = "123.45"
    
    print("\n--- Type Conversion ---")
    if isinstance(raw_input, str):
        val_float = float(raw_input)
        val_int = int(val_float)
        print(f"String '{raw_input}' converted to float: {val_float} and int: {val_int}")
    # --- Type Conversion ---
    #String '123.45' converted to float: 123.45 and int: 123

# Execute the exercise
if __name__ == "__main__":
    run_builtin_exercise()