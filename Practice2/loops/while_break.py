# When you do need terminate the loop no matter condition is True or False
# You could use keyword break for this:

i = 1
while i < 113e12:
  print(i)
  if i == 3:
    break
  i += 1