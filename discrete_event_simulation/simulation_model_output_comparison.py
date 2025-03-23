import os
import matplotlib.pyplot as plt

class SimulationModelOutputComparison:
    """
    Defines the comparison framework for simulation model outputs.

    This class is designed to compare the outputs of two simulation models – the original (unoptimised) model and
    the cost-optimised model – by generating a series of visualisations that highlight differences in resource
    allocation, wait times, and overall performance. It also utilises regression data to produce residuals and
    other statistical plots for further analysis.

    The class consists of the following functions:
      
    1. __init__(original_model, optimised_model, reg_data, figures_location):
       a. Used to initialise the comparison object with the original and cost-optimised simulation models as well as
          the regression data. It also sets the directory for saving all generated figures, creating the directory
          if it does not already exist.
      
    2. plot_difference_resources():
       a. Plots a bar chart comparing the resource quantities between the original and cost-optimised models.
      
    3. plot_difference_bar(original_quantity, optimised_quantity, labels, labels_plot, Title_of_plot="Comparison of Resources: Original vs Cost-Optimised", X_label="Resources", Y_label="Resource Value"):
       a. A generic method to generate a bar chart comparing two sets of values (e.g., resource counts, average wait times)
          with customisable titles, labels, and axis descriptions.
      
    4. plot_avg_times():
       a. Computes and plots the average wait times for specified processes from both simulation models.
      
    5. plot_utilisation_rates():
       a. Calculates and visualises the resource utilisation rates (as a percentage of busy time) for both the original
          and cost-optimised models.
      
    6. plot_residuals_probplot():
       a. Generates a Q-Q (probability) plot for the residuals obtained from the regression analysis to assess the
          normality of the residuals.
      
    7. plot_arrival_vs_total_time():
       a. Creates a scatter plot comparing patient arrival times to the total time spent in the emergency department
          for both simulation models.
      
    8. plot_resource_wait_time_boxplots():
       a. Produces box plots that display the distribution of resource wait times for the original and cost-optimised models.

    The class has the following attributes:
       1. original_model: The simulation model instance representing the unoptimised scenario.
       2. optimised_model: The simulation model instance representing the cost-optimised scenario.
       3. keys: A list of resource keys extracted from the simulation models.
       4. data_keys: A list of column names (from the collated simulation data) corresponding to process wait times.
       5. mlr_data: A list containing the multiple linear regression model and its associated data (features, targets, predictions).
       6. op_dir: The directory where all generated figures are saved.
    """
    def __init__(self, original_model, optimised_model, figures_location):
        self.original_model = original_model
        self.optimised_model = optimised_model
        self.figures_location = figures_location
        if not os.path.exists(self.figures_location):
            os.makedirs(self.figures_location)

    def plot_difference_resources(self):
        plt.figure()
        plt.title("Resource Allocation Comparison")
        plt.bar(self.original_model.resource_dict.keys(), self.original_model.resource_dict.values(), label="Original")
        plt.bar(self.optimised_model.resource_dict.keys(), self.optimised_model.resource_dict.values(), label="Optimised")
        plt.legend()
        plt.savefig(os.path.join(self.figures_location, "resource_comparison.png"))

