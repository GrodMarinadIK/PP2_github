import math

# 1. Degree to Radian
degree = 180
radian = math.radians(degree)
print(f"Input degree: {degree}\nOutput radian: {radian:.6f}")

# 2. Area of a trapezoid
h = 5
base1 = 5
base2 = 6
area_trap = 0.5 * (base1 + base2) * h
print(f"Trapezoid area: {area_trap}")

# 3. Area of regular polygon
sides = 4
length = 25
# Formula: (n * s^2) / (4 * tan(pi/n))
area_poly = (sides * length**2) / (4 * math.tan(math.pi / sides))
print(f"Polygon area: {area_poly}")

# 4. Area of a parallelogram
p_base = 5
p_height = 6
print(f"Parallelogram area: {float(p_base * p_height)}")