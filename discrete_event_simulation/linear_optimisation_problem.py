import pulp

class LinearOptimisationProblem:
    """
    Defines the linear optimisation problem for minimising the Length of Stay (LOS) in the emergency department.

    This class sets up and solves a linear programming problem based on a multiple linear regression (MLR) model.
    It determines the optimal allocation of hospital resources that minimizes the predicted LOS while adhering to a
    budget constraint. The optimisation is performed using PuLP.

    The class consists of the following functions:

    1. __init__(resource_dict, intercept, coefficient_vector_dict, lower_bound_list, upper_bound_list, cost_dict, max_cost=11000):
       a. Used to initialise the optimisation problem with the given resource dictionary, regression intercept,
          MLR coefficients, lower and upper bounds for each resource, and the cost dictionary. The maximum allowable
          cost is set via max_cost. During initialisation, it also prints the intercept, each resource’s coefficient,
          and the unoptimised total cost of resources.

    2. initialise_problem():
       a. Creates the decision variables for each resource (with specified lower and upper bounds) and sets up the
          objective function (the predicted LOS) along with the budget constraint in the PuLP problem.

    3. solve():
       a. Solves the linear optimisation problem and stores the optimal resource allocation in the attribute
          'optimal_resource_dict'.

    4. depict_results():
       a. Prints the optimisation status, the optimal LOS value, the optimal allocation for each resource, and the
          total cost of the optimised resources.

    The class has the following attributes:
       1. problem: The PuLP linear programming problem instance.
       2. lower_bounds: List of lower bound constraints for each resource.
       3. upper_bounds: List of upper bound constraints for each resource.
       4. resource_dict: Dictionary mapping each resource to its initial count.
       5. resource_keys: List of resource names extracted from resource_dict.
       6. beta0: The intercept from the regression model.
       7. beta: Dictionary of MLR coefficients for each resource.
       8. cost: Dictionary mapping each resource to its cost.
       9. max_bound: Maximum allowable total cost of resources.
       10. resource_variables: The PuLP decision variables representing the number of each resource.
       11. optimal_resource_dict: Dictionary storing the optimal allocation of resources after solving the problem.
    """
    def __init__(self, resource_dict, intercept, coefficients, lower_bounds, upper_bounds, cost_dict, max_cost=11000):
        self.problem = pulp.LpProblem("Minimize_LOS", pulp.LpMinimize)
        self.resource_dict = resource_dict
        self.resource_keys = list(resource_dict.keys())
        self.intercept = intercept
        self.coefficients = coefficients
        self.cost_dict = cost_dict
        self.max_cost = max_cost
        self.resource_variables = {key: pulp.LpVariable(key, lowBound=lower_bounds[i], upBound=upper_bounds[i], cat='Integer')
                                   for i, key in enumerate(self.resource_keys)}

    def initialise_problem(self):
        self.problem += self.intercept + sum(self.coefficients[key] * self.resource_variables[key] for key in self.resource_keys), "Total_LOS"
        self.problem += sum(self.cost_dict[key] * self.resource_variables[key] for key in self.resource_keys) <= self.max_cost, "Budget_Constraint"

    def solve(self):
        self.problem.solve()
        self.optimal_resources = {key: int(pulp.value(self.resource_variables[key])) for key in self.resource_keys}

