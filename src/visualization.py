import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Get the base directory of the script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define correct results file path (inside "src/results/")
results_path = os.path.join(base_dir, "results", "optimized_routes.csv")

# Ensure the results file exists
if not os.path.exists(results_path):
    print(f"❌ ERROR: Results file not found -> {results_path}")
    exit(1)

# Load the optimized shipment data
results = pd.read_csv(results_path)

# Ensure required columns exist
if 'Seller ID' not in results.columns:
    print("❌ ERROR: 'Seller ID' column missing in results file!")
    exit(1)

# Count the number of shipments per seller
shipment_counts = results['Seller ID'].value_counts()

# Plot the data
plt.figure(figsize=(12, 6))
sns.barplot(x=shipment_counts.index, y=shipment_counts.values, palette="Blues_r")

plt.xlabel("Seller ID", fontsize=12)
plt.ylabel("Number of Shipments", fontsize=12)
plt.title("📦 Number of Orders Fulfilled by Each Seller", fontsize=14)
plt.xticks(rotation=90)  # Rotate seller IDs for readability

# Ensure the plots directory exists inside "src/results/"
plots_dir = os.path.join(base_dir, "results", "plots")
os.makedirs(plots_dir, exist_ok=True)  # Creates the directory if it does not exist

# Save the plot as an image
plot_path = os.path.join(plots_dir, "shipment_distribution.png")
plt.savefig(plot_path, bbox_inches="tight")

# Show the plot
plt.show()

print(f"✅ Plot saved successfully at: {plot_path}")
