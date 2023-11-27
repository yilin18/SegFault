import random
import csv
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker to generate realistic fake data
fake = Faker()

# Define the number of records
num_users = 30000
num_products = 10000
num_categories = 100
num_orders = 7000
num_order_details = 30000  # Each order has several products

# Helper function to generate a random date within the last year
def random_date():
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    return fake.date_between(start_date=start_date, end_date=end_date)

# A function to write the data to CSV files
def write_to_csv(file_name, data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Paths for CSV files
csv_file_names = {
    "users": "users.csv",
    "products": "products.csv",
    "categories": "categories.csv",
    "orders": "orders.csv",
    "order_details": "order_details.csv"
}

# Generate and write data for Users
users = [{
    "UserID": i + 1,
    "Name": fake.name(),
    "Email": fake.email(),
    "Address": fake.address(),
    "Password": fake.password()
} for i in range(num_users)]
write_to_csv(csv_file_names["users"], users)

# Generate and write data for Categories
categories = [{
    "CategoryID": i + 1,
    "Name": fake.word(),
    "Description": fake.text(max_nb_chars=50)
} for i in range(num_categories)]
write_to_csv(csv_file_names["categories"], categories)

# Generate and write data for Products
products = [{
    "ProductID": i + 1,
    "Name": fake.word(),
    "Description": fake.text(max_nb_chars=100),
    "Price": round(random.uniform(1, 1000), 2),
    "StockQuantity": random.randint(0, 100),
    "CategoryID": random.randint(1, num_categories)
} for i in range(num_products)]
write_to_csv(csv_file_names["products"], products)

# Generate and write data for Orders
orders = []
order_details = []
for i in range(num_orders):
    user_id = random.randint(1, num_users)
    order_date = random_date()
    order = {
        "OrderID": i + 1,
        "UserID": user_id,
        "Date": order_date,
        "TotalPrice": 0,  # To be updated
        "Status": random.choice(["Pending", "Shipped", "Delivered"])
    }
    orders.append(order)

    # Generate OrderDetails for this order
    num_items = random.randint(1, 10)
    for _ in range(num_items):
        product_id = random.randint(1, num_products)
        quantity = random.randint(1, 10)
        price_per_unit = products[product_id - 1]["Price"]
        total_price = round(quantity * price_per_unit, 2)
        order["TotalPrice"] += total_price
        order_details.append({
            "OrderID": i + 1,
            "ProductID": product_id,
            "Quantity": quantity,
            "PricePerUnit": price_per_unit
        })

write_to_csv(csv_file_names["orders"], orders)
write_to_csv(csv_file_names["order_details"], order_details)

print("Data generation complete. CSV files created.")
