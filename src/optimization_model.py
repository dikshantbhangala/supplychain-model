import pandas as pd
import os
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value, GUROBI

# Get the base directory of the script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define correct data file path (inside "src/data2/")
data_path = os.path.join(base_dir, "data2", "cleaned_supply_chain_data.csv")

# Ensure the cleaned data file exists
if not os.path.exists(data_path):
    print(f"❌ ERROR: Data file not found -> {data_path}")
    exit(1)

# Load only the first 1000 entries from the cleaned supply chain data
df = pd.read_csv(data_path, nrows=1000)  # Change to nrows=500 if needed

# Ensure required columns exist
required_columns = {'seller_id', 'order_id', 'freight_value'}
if not required_columns.issubset(df.columns):
    print(f"❌ ERROR: Missing required columns in data file! Found columns: {df.columns}")
    exit(1)

# Get unique sellers and orders
sellers = df['seller_id'].unique()
orders = df['order_id'].unique()

# Define optimization variables
x = {(i, j): LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for i in sellers for j in orders}

# Define the optimization model
model = LpProblem("Supply_Chain_Optimization", LpMinimize)

# Define the objective function (minimizing freight cost)
model += lpSum(x[i, j] * df.loc[(df['seller_id'] == i) & (df['order_id'] == j), 'freight_value'].sum()
               for i in sellers for j in orders), "Total Freight Cost"

# Ensure each order is fulfilled by at least one seller
for j in orders:
    model += lpSum(x[i, j] for i in sellers) >= 1, f"Order_{j}_Fulfillment"

# Solve using Gurobi (FASTEST SOLVER)
model.solve(GUROBI())

# Print and save results
if model.status == 1:  # Status 1 means "Optimal Solution Found"
    print("✅ Optimal Solution Found:")
    results = [(i, j, value(x[i, j])) for i, j in x if value(x[i, j]) > 0]

    for i, j, units in results:
        print(f"📦 Ship {units} units from Seller {i} to Order {j}")

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results, columns=['Seller ID', 'Order ID', 'Units Shipped'])

    # Ensure the save directory exists inside "src/results"
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)  # Creates the directory if it does not exist

    # Save the results inside "src/results/optimized_routes.csv"
    results_path = os.path.join(results_dir, "optimized_routes.csv")
    results_df.to_csv(results_path, index=False)
    print(f"✅ Optimization complete! Results saved at: {results_path}")

else:
    print("❌ No optimal solution found. Check constraints and data.")
