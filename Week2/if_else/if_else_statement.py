# two-sided choice:
LH = 44
MV = 33

if LH > MV:
    print("LH is greater than MV")    
else:
    print("LH is not greater than MV")
    
# Logical operators:
c = 300
if LH > MV and c > MV:
    print("Both conditions are True")

if LH > MV or MV > c:
    print("At least one is True")
    
if not LH > MV > c:
    print("at least one is False")
    
# Nested if (Вложенные условия)
x = 16
if x > 10:
    print("Above ten,", end="")
    if x > 20:
        print(" and also above 20")
    else:
        print(" and less than 20")

