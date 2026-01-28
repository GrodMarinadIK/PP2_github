# random numbers
import random 
print("Random integer from 1 to 10: ", random.randrange(1, 10))


x = 1               # int
y = 2.2             # float
z = 53 + 4j         # complex

# Converting types:
x1 = float(x)       # int -> float (1.0)
y1 = int(y)         # float -> int (2) 
y2 = complex(y)     # float -> complex (2.2 + 0j)

a = -12             # int, just negative
b = -23.5           # float, just negative
c = -23 - 2j        # complex, just negative

# float scientific:

t = 35e3            # = 35 * 10^{3}
t2 = 12E4           # = 12 * 10^{4}
t3 = -87.7e100      # = -87.7 * 10^{100}
