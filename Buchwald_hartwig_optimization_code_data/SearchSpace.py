from baybe.targets import NumericalTarget
from baybe.objectives import SingleTargetObjective
from baybe.searchspace import SearchSpace
from baybe import Campaign
import pandas as pd
from pathlib import Path

target = NumericalTarget(name="Yield")
objective = SingleTargetObjective(target=target)

from baybe.parameters import (
    NumericalDiscreteParameter,
    CustomDiscreteParameter,
    CategoricalParameter,
)

coupling_partner_equiv = NumericalDiscreteParameter("Coupling partner loading (equiv)", values = (1.0, 1.2,1.5))

base_equiv = NumericalDiscreteParameter("Base loading (equiv)", values = (1.0, 2.0, 3.0))

catalyst_equiv = NumericalDiscreteParameter(name = "Catalyst loading (mol%)", values = (1, 3, 5 ))

temperature = NumericalDiscreteParameter("Temperature (°C)", values = (120, 130, 140))

residence_time = NumericalDiscreteParameter("Residence time (min)", values = ( 30, 40, 50, 60,))

base_type = CategoricalParameter("Base type", values = ("BTMG", "DBU", "TMG"), encoding = "OHE")

ligands = pd.read_csv("ligand_descriptors.csv")

descriptor_df = (
    ligands[
        [
        "Catalyst",
        "vbur_vbur_min",
        "vmin_vmin_boltz",
        ]
    ]
    .set_index("Catalyst")
)

catalyst = CustomDiscreteParameter(
    name="Catalyst",
    data=descriptor_df,
)

parameters = [coupling_partner_equiv,
                   base_equiv,
                   catalyst_equiv,
                   temperature,
                   residence_time,
                   base_type, 
                   catalyst]

searchspace = SearchSpace.from_product(parameters)

if Path("campaign.json").exists():
    campaign = Campaign.from_json("campaign.json")
    print("Existing campaign loaded.")
    print(
        f"Measurements loaded: "
        f"{len(campaign.measurements)}"
    )
else:
    campaign = Campaign(searchspace, objective)
    print("New campaign created.")   

while True:
    recommendation = campaign.recommend(batch_size=2)
    print(recommendation)
    
    yields = []
    for i in range (len(recommendation)):
        y = float(input(f"Enter the yield for experiment {i+1}: "))
        yields.append(y)

    recommendation["Yield"] = yields

    campaign.add_measurements(recommendation)
    campaign.to_json(
        "campaign.json", 
        overwrite=True,
        )
    
    print("\nCampaign updated.")
    
    cont = input("\nDo you want to stop? (y/n): ")
    
    if cont.lower() == "y":
        break
    
