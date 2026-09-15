import pandas as pd

# Load all datasets
files = [
    "Validation_data_p2et.csv",       # P2Et
    "Validation_data_BTMG.csv",  # BTMG
    "Validation_data_MTBD.csv"   # MTBD
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Ensure additive is treated consistently
df["Additive"] = df["Additive"].astype(str)

while True:
    # User input
    ligand = input("Ligand: ").strip()
    base = input("Base: ").strip()
    additive = input("Additive (none, 1-7): ").strip()

    # Find matching row
    result = df[
        (df["Ligand"] == ligand) &
        (df["Base"] == base) &
        (df["Additive"] == additive)
    ]

    if len(result) > 0:
        yield_value = result.iloc[0]["Yield"]
        print(f"Yield = {yield_value}%")
    else:
        print("Combination not found.")
    
    action  = input("Do you want to search again? (yes/no): ").strip().lower()
    if action == "no":
        break