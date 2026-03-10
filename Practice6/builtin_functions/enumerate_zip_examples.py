from functools import reduce

def process_numbers(data):
    # map: transform every element
    doubled = list(map(lambda x: x * 2, data))
    
    # filter: remove elements that don't match criteria
    greater_than_10 = list(filter(lambda x: x > 10, doubled))
    
    # reduce: aggregate all into one value
    total = reduce(lambda x, y: x + y, greater_than_10)
    
    return total

def get_stats(data):
    # Built-in math functions: min, max, sum, len
    return {
        "min": min(data),
        "max": max(data),
        "sum": sum(data),
        "len": len(data)
    }