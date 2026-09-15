import pandas as pd
from baybe import Campaign

manual_measurement = pd.DataFrame({
    "Coupling partner loading (equiv)": [1.2],
    "Base loading (equiv)": [3.0],
    "Catalyst loading (mol%)": [3.0],
    "Temperature (°C)": [140.0],
    "Residence time (min)": [60.0],
    "Base type": ["BTMG"],
    "Catalyst": ["EphosPdG4"],
    "Yield": [25.0]
})

campaign = Campaign.from_json("campaign.json")
campaign.add_measurements(manual_measurement)
campaign.to_json(
        "campaign.json", 
        overwrite=True,
        )
