from discrete_event_simulation import SimpySimulation, LinearOptimisationProblem, SimulationModelOutputComparison
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

process_list = [
        ["Stretcher Allocation", ["Stretcher"],[10,15]],
        ["Patient Doc Check", [ "Doctor","Para Staff"],[10,30]],
        ["Payment Check", ["Bill Counter"],[5,20]],
        ["Lab Investigation", ["Lab Eqpt"],[15,120]],
        ["Ultrasonic Investigation", ["UltraSound"],[10,20]],
        ["Re-Examination Doc Check", ["ED Doc","Para Staff"],[10,45]],
        ["Surgery Ward Allocation", ["Surgery Staff"],[15,25]],
        ["Surgeon Check", ["Surgeon"],[10,20]],
        ["Specialist Ward Allocation", ["Specialist Staff"],[5,15]],
        ["Specialist Check", ["Specialist"],[5,20]],
        ["Operating Theatre Allocation", ["Orthodoctor"],[20,45]]
    ]

resource_dict = {
"Stretcher": 2,
"ED Doc": 1,
"Para Staff": 2,
"Bill Counter": 3,
"Lab Eqpt": 2,
"UltraSound":2,
"Surgeon": 1,
"Surgery Staff": 1,
"Specialist": 1,
"Specialist Staff": 2,
"Orthodoctor": 1,
"Doctor":1
}
log_process_list = ["Ultrasonic Investigation", "Lab Investigation", "Surgery Ward Allocation", "Specialist Ward Allocation"]

def main():
    sim = SimpySimulation(resource_dict, process_list, log_process_list)
    sim.begin()
    sim.store_data("unoptimised_simulation.csv")

    data = pd.read_csv("unoptimised_simulation.csv")
    x_train, x_test, y_train, y_test = train_test_split(data.iloc[:, 1:-1], data.iloc[:, -1])
    reg = LinearRegression().fit(x_train, y_train)

    opt_problem = LinearOptimisationProblem(resource_dict, reg.intercept_, dict(zip(resource_dict.keys(), reg.coef_)),
                                            [1, 1, 1], [3, 3, 3], {"Stretcher": 500, "Doctor": 1000, "Para Staff": 400})
    opt_problem.initialise_problem()
    opt_problem.solve()

    optimised_sim = SimpySimulation(opt_problem.optimal_resources, process_list, log_process_list)
    optimised_sim.begin()
    optimised_sim.store_data("optimised_simulation.csv")

if __name__ == "__main__":
    main()

