from baybe import Campaign
from Yield_exp_extractor import extract_yield_and_experiment

def extract_reaction_conditions(campaign_json_path):
    """Extracts all reaction conditions (parameter values) from a campaign JSON file."""
    campaign = Campaign.from_json(campaign_json_path)

    measurements = campaign.measurements

    measurements = measurements.reset_index(drop=True)
    measurements["Experiment"] = measurements.index + 1

    condition_columns = [p.name for p in campaign.parameters]

    return measurements[["Experiment"] + condition_columns]

def export_conditions_and_yield(campaign_json_path, csv_path):
    """Exports reaction conditions and their corresponding yield to a CSV file."""
    conditions = extract_reaction_conditions(campaign_json_path)
    yields = extract_yield_and_experiment(campaign_json_path)

    combined = conditions.merge(yields, on="Experiment")
    combined.to_csv(csv_path, index=False)

    return combined

if __name__ == "__main__":
    file_name = input("Enter the file name for the campaign you want to export. E.g. campaign.json: ")
    csv_name = input("Enter the output CSV file name. E.g. campaign_results.csv: ")
    export_conditions_and_yield(file_name, csv_name)
    print(f"Exported conditions and yield to {csv_name}")
