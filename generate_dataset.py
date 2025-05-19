import random
import csv
from datetime import datetime, timedelta

# Original product data
products = [
    {"ID": 1, "Product Name": "Mobile", "Price": 20000},
    {"ID": 2, "Product Name": "mouse", "Price": 500},
    {"ID": 3, "Product Name": "laptop-lenova", "Price": 50000},
    {"ID": 4, "Product Name": "keyboard", "Price": 500},
    {"ID": 5, "Product Name": "charger", "Price": 2000},
    # {"ID": 6, "Product Name": "Flour", "Price": 150},
    # {"ID": 7, "Product Name": "Bottel", "Price": 100},
    # {"ID": 8, "Product Name": "Box", "Price": 200},
    {"ID": 9, "Product Name": "Earphones", "Price": 1200},
    {"ID": 10, "Product Name": "Monitor", "Price": 15000},
    {"ID": 11, "Product Name": "Pen Drive", "Price": 700},
    # {"ID": 12, "Product Name": "Notebook", "Price": 70},
    # {"ID": 13, "Product Name": "Washing Powder", "Price": 250},
    # {"ID": 14, "Product Name": "Hand Wash", "Price": 180},
    {"ID": 15, "Product Name": "USB Cable", "Price": 350},
    {"ID": 16, "Product Name": "Smartwatch", "Price": 5000},
    {"ID": 17, "Product Name": "LED Bulb", "Price": 100},
    # {"ID": 18, "Product Name": "Milk Packet", "Price": 60},
    # {"ID": 19, "Product Name": "Detergent Bar", "Price": 50},
    # {"ID": 20, "Product Name": "Toothpaste", "Price": 120}
    {"ID": 21, "Product Name": "Honey", "Price": 450},
    {"ID": 22, "Product Name": "Almond ", "Price": 600},
    {"ID": 23, "Product Name": "Granola Bar", "Price": 120}

]


# Configurable parameters
start_date = datetime(2025, 3, 1)
end_date = datetime(2025, 3, 30)
num_entries_per_product = 25  # how many samples per product

# Generate random data
def generate_random_data():
    data = []
    record_id = 1  # start ID for new records
    for product in products:
        for _ in range(num_entries_per_product):
            sales = random.randint(1, 15)
            discount = random.choice([0, 2, 5, 10, 15])
            price_variation = product["Price"] * random.uniform(0.7, 1.3)
            price = round(price_variation, 2)
            random_days = random.randint(0, (end_date - start_date).days)
            random_seconds = random.randint(0, 86400)  # seconds in a day
            random_date = start_date + timedelta(days=random_days, seconds=random_seconds)
            stock_quantity = random.randint(5, 20)

            data.append([
                record_id,
                product["Product Name"],
                sales,
                discount,
                price,
                random_date.strftime("%B %d, %Y, %I:%M %p"),
                stock_quantity
            ])
            record_id += 1
    return data

# Save to CSV
def save_to_csv(data, filename="generated_product_data.csv"):
    headers = ["ID", "Product Name", "Sales", "Discount (%)", "Price", "Date Recorded", "Stock Quantity"]
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"✅ Data saved to {filename}")

# Main
if __name__ == "__main__":
    generated_data = generate_random_data()
    save_to_csv(generated_data)
