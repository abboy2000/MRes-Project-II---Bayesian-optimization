from baybe.targets import NumericalTarget
from baybe.objectives import SingleTargetObjective
from baybe.searchspace import SearchSpace
from baybe import Campaign
import pandas as pd
from pathlib import Path
from baybe.recommenders import *
from baybe.parameters import (
    CustomDiscreteParameter,
    CategoricalParameter,
)
from baybe.acquisition.acqfs import qLogExpectedImprovement, qUpperConfidenceBound, qProbabilityOfImprovement
from baybe.surrogates import RandomForestSurrogate

def run_optimization(campaign_name, acq_func=None, surrogate=None, initial_recommender_type=None):
    """Runs the optimization process for a given campaign."""
    
    target = NumericalTarget(name="Yield")
    objective = SingleTargetObjective(target=target)


    base = CategoricalParameter("Base", values = ["P2Et", "MTBD", "BTMG"], encoding = "OHE")

    ligands = pd.read_csv("Ligand_descriptors.csv")
    ligands_df = (
        ligands[
            [
            "Ligand",
            "vmin_vmin_boltz",
            "vbur_vbur_min", 
            ]
        ]
        .set_index("Ligand")
    )

    ligand = CustomDiscreteParameter(
        name="Ligand",
        data=ligands_df,
    )

    additives = pd.read_csv("Descriptors_additives.csv")
    additives_df = (
        additives[
            [
            "Additive",
            "HOMO",
            "Softness",
            "SASA",
            ]
        ]
        .set_index("Additive")
    )      

    additive = CustomDiscreteParameter(
        name="Additive",
        data=additives_df,
    )

    parameters = [base, ligand, additive]
    searchspace = SearchSpace.from_product(parameters)
    
    if acq_func and surrogate is None:
        botorch = BotorchRecommender()
    elif acq_func is None and surrogate is not None:
        botorch = BotorchRecommender(surrogate_model=surrogate)
    else:
        botorch = BotorchRecommender(acquisition_function=acq_func)
    
    if initial_recommender_type is None:
        recommender = TwoPhaseMetaRecommender(
    initial_recommender=RandomRecommender(),  
    recommender=botorch, 
    )
    else:
        recommender= TwoPhaseMetaRecommender(
            initial_recommender=initial_recommender_type,
            recommender=botorch,
            )

    if Path(campaign_name).exists():
        campaign = Campaign.from_json(campaign_name)
        print("Existing campaign loaded.")
    else:
        campaign = Campaign(searchspace, objective, recommender)
        print("New campaign created.") 
        
    while True:
        recommendation = campaign.recommend(batch_size=3)
        print(recommendation)
        
        yields = []
        for i in range (len(recommendation)):
            y = float(input(f"Enter the yield for experiment {i+1}: "))
            yields.append(y)

        recommendation["Yield"] = yields

        campaign.add_measurements(recommendation)
        campaign.to_json(
            campaign_name,
            overwrite=True,
            )
        print("\nCampaign updated.")
        
        cont = input("\nDo you want to stop? (y/n): ")
        
        if cont.lower() == "y":
            break

