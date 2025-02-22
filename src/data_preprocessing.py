import pandas as pd
import os

# Get the base directory (where this script is located)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct correct file paths
data_dir = os.path.join(base_dir, "..", "data")  # Move up one level and access 'data'
orders_path = os.path.join(data_dir, "olist_orders_dataset.csv")
order_items_path = os.path.join(data_dir, "olist_order_items_dataset.csv")
sellers_path = os.path.join(data_dir, "olist_sellers_dataset.csv")
geolocation_path = os.path.join(data_dir, "olist_geolocation_dataset.csv")

# Check if the files exist before reading
for path in [orders_path, order_items_path, sellers_path, geolocation_path]:
    if not os.path.exists(path):
        print(f"❌ ERROR: File not found -> {path}")
        exit(1)  # Stop execution if any file is missing

# Load datasets
orders = pd.read_csv(orders_path)
order_items = pd.read_csv(order_items_path)
sellers = pd.read_csv(sellers_path)
geolocation = pd.read_csv(geolocation_path)

print("✅ Datasets loaded successfully!")


# Display dataset samples
print("\nOrders Dataset: \n", orders.head())
print("\nOrder Items Dataset: \n", order_items.head())
print("\nSellers Dataset: \n", sellers.head())
print("\nGeolocation Dataset: \n", geolocation.head())

# Ensure correct column names exist before selecting
orders = orders[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp']]
order_items = order_items[['order_id', 'product_id', 'seller_id', 'price', 'freight_value']]
sellers = sellers[['seller_id', 'seller_zip_code_prefix']]
geolocation = geolocation[['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']]

# Merge datasets
merged_data = order_items.merge(orders, on='order_id', how='left')
merged_data = merged_data.merge(sellers, on='seller_id', how='left')
merged_data = merged_data.merge(geolocation, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')

# Drop redundant columns
merged_data.drop(columns=['seller_zip_code_prefix', 'geolocation_zip_code_prefix'], inplace=True)

# Define absolute save path
save_path = os.path.join(base_dir, "data", "cleaned_supply_chain_data.csv")

# Ensure the directory exists before saving
save_dir = os.path.dirname(save_path)
if not os.path.exists(save_dir):  
    os.makedirs(save_dir)  # ✅ Creates the directory if it does not exist

# Save the cleaned data
merged_data.to_csv(save_path, index=False)

print(f"Cleaned data saved successfully at: {save_path}")
