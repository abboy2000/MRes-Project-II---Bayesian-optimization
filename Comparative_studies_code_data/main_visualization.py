from Yield_exp_extractor import extract_yield_and_experiment
from visualization import plot_y_vs_exp, shap_insight
import matplotlib.pyplot as plt

file_name = input("Enter the file name for the campaign you want to visualize. E.g. campaign.json: ")
yield_df = extract_yield_and_experiment(file_name)
plot_y_vs_exp(yield_df)
plt.figure()
shap_insight(file_name)
plt.show()