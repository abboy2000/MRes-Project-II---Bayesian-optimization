from baybe import Campaign

def extract_yield_and_experiment(campaign_json_path):
    """Extracts Yield and Experiment Number from a campaign JSON file."""
    campaign = Campaign.from_json(campaign_json_path)

    measurements = campaign.measurements

    measurements = measurements.reset_index(drop=True)
    measurements["Experiment"] = measurements.index + 1

    return measurements[["Experiment","Yield"]]

  