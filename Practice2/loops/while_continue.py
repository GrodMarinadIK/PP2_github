# With the continue statement we can stop the current iteration, 
# and continue with the next
# Using other words you could "skip" step with continue


i = 0
while i < 10:
  i += 1
  if i == 3:
    continue
  print(i)
