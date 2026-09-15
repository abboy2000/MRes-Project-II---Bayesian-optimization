import matplotlib.pyplot as plt
from baybe import Campaign
from baybe.insights import SHAPInsight


def plot_y_vs_exp(json_file):
    """Plots Yield vs Experiment Number using data extracted from a JSON file."""
    plt.plot(
        json_file["Experiment"],
        json_file["Yield"],
        marker="o"
    )

    plt.xlabel("Experiment Number")
    plt.ylabel("Yield (%)")
    plt.title("Yield vs Experiment")

def load_campaign(file_path):
    """Loads a campaign from a JSON file."""
    return Campaign.from_json(file_path)


def shap_insight(file_path):
    """Displays the shap insight plot for the campaign."""
    campaign = load_campaign(file_path)
    insight = SHAPInsight.from_campaign(campaign)
    insight.plot("bar")

