def organize_data(names, scores):
    # zip: combine two lists into pairs
    # sorted: sort by score (the second element of the tuple)
    paired = zip(names, scores)
    sorted_data = sorted(paired, key=lambda x: x[1], reverse=True)
    
    # enumerate: loop with index
    for index, (name, score) in enumerate(sorted_data):
        print(f"Rank {index + 1}: {name} with score {score}")

def type_conversions(value):
    # Type conversion functions
    # Always good to have these under control
    return {
        "as_int": int(value),
        "as_float": float(value),
        "as_str": str(value),
        "as_list": list(str(value))
    }