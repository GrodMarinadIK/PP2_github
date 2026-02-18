import datetime as dt

# 1. Subtract five days
five_days_ago = dt.datetime.now() - dt.timedelta(days=5)
print(f"Five days ago: {five_days_ago}")

# 2. Yesterday, today, tomorrow
today = dt.datetime.now()
yesterday = today - dt.timedelta(days=1)
tomorrow = today + dt.timedelta(days=1)
print(f"Yesterday: {yesterday.date()}, Today: {today.date()}, Tomorrow: {tomorrow.date()}")

# 3. Drop microseconds
now_no_micro = dt.datetime.now().replace(microsecond=0)
print(f"Without microseconds: {now_no_micro}")

# 4. Difference in seconds
date1 = dt.datetime(2026, 2, 20, 12, 0, 0)
date2 = dt.datetime(2026, 2, 17, 12, 0, 0)
diff = (date1 - date2).total_seconds()
print(f"Difference in seconds: {diff}")