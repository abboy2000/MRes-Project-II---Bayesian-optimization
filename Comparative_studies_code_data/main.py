from BaybeSearchspaceScript import run_optimization
from baybe.recommenders import (
    FPSRecommender,
    KMeansClusteringRecommender,
)
from baybe.acquisition.acqfs import qLogExpectedImprovement, qUpperConfidenceBound, qProbabilityOfImprovement
from baybe.surrogates import RandomForestSurrogate

def main():
    file_name = input("Enter the file name for the campaign. E.g. campaign.json: ")
    initial_recommender_type = input("Enter the initial recommender type (FPS, Kmeans) or leave for default: ")
    
    if initial_recommender_type.lower() == "":
        initial_recommender_type = None
    elif initial_recommender_type.lower() == "fps":
        initial_recommender_type = FPSRecommender()
    elif initial_recommender_type.lower() == "kmeans":
        initial_recommender_type = KMeansClusteringRecommender()
    
    acq_func_input = input("Enter the acquisition function (EI, UCB, PI) or leave for default: ")
    if acq_func_input.lower() == "":
        acq_func = None
    elif acq_func_input.lower() == "ei":
        acq_func = qLogExpectedImprovement()
    elif acq_func_input.lower() == "ucb":
        acq_func = qUpperConfidenceBound()
    elif acq_func_input.lower() == "pi":
        acq_func = qProbabilityOfImprovement()
    
    surrogate_input = input("Enter the surrogate model (RandomForest) or leave for default: ")
    if surrogate_input.lower() == "":
        surrogate = None
    elif surrogate_input.lower() == "randomforest":
        surrogate = RandomForestSurrogate()

    
    run_optimization(file_name, acq_func, surrogate, initial_recommender_type)  # You can change the recommender type as needed

    
if __name__ == "__main__":
    main()