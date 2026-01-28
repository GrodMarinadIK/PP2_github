# chain of conditions
score = 75
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: D")

# Заглушка pass
# Если условие есть, а кода пока нет — использоват pass, чтобы не было ошибки
# If there exists condition, but there is no code - use pass for avoiding errors
a = 33
b = 200
if b > a:
    pass
