import re
import json
import os 

current_dir = os.path.dirname(__file__)
path_to_raw_txt = os.path.join(current_dir, 'raw.txt')
path_to_receipt_json = os.path.join(current_dir, 'receipt.json')
# Читаем исходник
with open(path_to_raw_txt, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract date and time
#                          DD.MM.YYYY           HH:MM:SS
dt_match = re.search(r"(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})", content)
date_time = dt_match.group(1) if dt_match else "Unknown"

# 2.Extract type of payment
payment_method = "Банковская карта" if "Банковская карта" in content else "Наличные"

# 3. Extract products and prices
products = []
    # \d+\.\n - position, (.*?) - name of a product, \n.*?\n - skipping information, ([\d\s]+,00) - price,
    # re.DOTALL - is for dot to see line breaks
items = re.findall(r"\d+\.\n(.*?)\n.*?\n([\d\s]+,00)", content, re.DOTALL)

total_calculated = 0
for name, price_str in items:
    clean_name = name.replace('\n', ' ').strip()
    # Deleting spaces between thousands and replacing comma with dot for float
    # e.g. 1 500 -> 1500; 1500,00 -> 1500.00;
    price_val = float(price_str.replace(' ', '').replace(',', '.'))
    
    products.append({
        "product": clean_name,
        "price": price_val
    })
    total_calculated += price_val

# Final dictionary
receipt_data = {
    "store": "EUROPHARMA",
    "date_time": date_time,
    "payment_method": payment_method,
    "items": products,
    "total_sum": total_calculated
}
# ensure_ascii=False - to see Cyrilic not the ascii references
print(json.dumps(receipt_data, indent=4, ensure_ascii=False))

with open(path_to_receipt_json, 'w', encoding='utf-8') as f:
    json.dump(receipt_data, f, indent=4, ensure_ascii=False)